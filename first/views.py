import json
import os
import shutil
import smtplib
from distutils.dir_util import copy_tree
from email.mime.text import MIMEText

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from first.models import BotFunctions, UsersBalance


def index(request):
    context = {}
    if request.method == "GET":
        print(request.GET)
    return render(request, "index.html", context)


def telegram_auth(request):
    context = {}
    return render(request, "telegram_auth.html", context)


def create_bot(request):
    context = {}
    print(os.getcwd())
    if request.method == "POST":
        if 'functions' in request.POST:
            function_names = request.POST.getlist('functions')
            print(function_names)
            if os.path.exists(os.getcwd() + "/BOT"):
                shutil.rmtree(os.getcwd() + "/BOT")
            os.mkdir(os.getcwd() + "/BOT")
            with open("BOT/BOT.py", "w") as bot:
                functions = []
                for name in function_names:
                    functions.append(BotFunctions.objects.get(func_name=name))
                with open("first/botTelegram/start_template.py", 'r') as start_file:
                    bot.write(start_file.read())
                for func in functions:
                    print(func.file_name)

                    if func.file_name == "stt.py":
                        files = os.listdir(os.getcwd() + "/first/botTelegram/for stt")
                        for fname in files:
                            shutil.copy2(os.path.join("first/botTelegram/for stt", fname), "BOT/")
                        if not os.path.exists(os.getcwd() + "/BOT/ready"):
                            os.mkdir(os.getcwd() + "/BOT/ready")
                        if not os.path.exists(os.getcwd() + "/BOT/voice"):
                            os.mkdir(os.getcwd() + "/BOT/voice")
                        with open(f'BOT/{func.file_name}', 'r') as file:
                            code = file.read()
                            bot.write(code)

                    elif func.file_name == "tts.py":
                        files = os.listdir(os.getcwd() + "/first/botTelegram/for tts")
                        for fname in files:
                            print(fname)
                            if os.path.isdir("first/botTelegram/for tts/" + fname):
                                copy_tree("first/botTelegram/for tts/" + fname, "BOT/models/")
                            else:
                                shutil.copy2(os.path.join("first/botTelegram/for tts", fname), "BOT/")
                        if not os.path.exists(os.getcwd() + "/BOT/ready"):
                            os.mkdir(os.getcwd() + "/BOT/ready")
                        if not os.path.exists(os.getcwd() + "/BOT/voice"):
                            os.mkdir(os.getcwd() + "/BOT/voice")
                        with open(f'BOT/{func.file_name}', 'r') as file:
                            code = file.read()
                            bot.write(code)
                    else:
                        with open(f'first/botTelegram/{func.file_name}', 'r') as file:
                            code = file.read()
                            bot.write(code)
                with open("first/botTelegram/end_template.py", 'r') as end_file:
                    bot.write(end_file.read())
            with open('BOT/config.json', 'w') as json_file:
                data = {}
                data["name"] = request.POST['name']
                data["username"] = request.POST['short_name']
                data["token"] = request.POST['token']
                json.dump(data, json_file)
            return redirect("../payment/")
    return render(request, "create_bot.html", context)

@login_required(login_url='/telegram_auth/')
def profile(request):
    """
        Страница профиля пользователя

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    try:
        user_balance = UsersBalance.objects.get(user_id=request.user.id)
        context['balance'] = user_balance.balance
    except:
        new_balance = UsersBalance(balance=0, user_id=request.user.id)
        new_balance.save()

    return render(request, "profile.html", context)


@login_required(login_url='/telegram_auth/')
def redact_profile(request, redact_profile_id):
    """
        Обработчик страницы редактирования профиля

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}

    if request.method == "POST":
        profile = User.objects.get(id=redact_profile_id)
        context["profile"] = profile
        profile.last_name = request.POST["last_name"]
        profile.email = request.POST["email"]
        profile.save()

    return render(request, "redact_profile.html", context)


def payment(request):
    context = {}
    return render(request, "payment.html", context)


def replenish(request):
    context = {}
    if True:
        print("POST!!!")
        summ = request.GET["sum"]
        if "payment_type_1" in request.GET:
            print(2)
            return HttpResponseRedirect(
                f"https://yoomoney.ru/quickpay/confirm.xml?receiver=4100118151035496&quickpay-form=button&sum={summ}&paymentType=PC&successURL=127.0.0.1&sum={summ}")
        else:
            print(3)
            return HttpResponseRedirect(
                    f"https://yoomoney.ru/quickpay/confirm.xml?receiver=4100118151035496&quickpay-form=button&sum={summ}&paymentType=AC")

    return render(request, "replenish.html", context)


def tech_support(request):
    context = {}
    if request.method == "POST":
        print("post")
        if 'email' in request.POST and 'email_text' in request.POST:
            message = request.POST['email_text']
            user_email = request.POST['email']
            sender = "botgod.sp@gmail.com"
            try:
                with open('first/email_password.json') as file:
                    password = json.load(file)["email_password"]
            except:
                print("pass error")
                return render(request, "tech_support.html", context)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            message += f"\n Почта пользователя: {user_email}"
            try:
                print(1)
                server.login(sender, password)
                msg = MIMEText(message)
                msg["Subject"] = "ЖАЛОБА ОТ ПОЛЬЗОВАТЕЛЯ"
                server.sendmail(sender, "andreysitalo09@gmail.com", msg.as_string())

                message = "Ваша жалоба отправлена и ожидает рассмотрения"
                msg = MIMEText(message)
                msg["Subject"] = "ЖАЛОБА ОТ ПОЛЬЗОВАТЕЛЯ"
                server.sendmail(sender, user_email, msg.as_string())

            except Exception as _ex:
                print(f"{_ex}\nCheck your login or password please!")

    return render(request, "tech_support.html", context)
