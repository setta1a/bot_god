import json
import os
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
        function_names = request.POST.getlist('functions')
        print(function_names)
        with open("BOT.py", "w") as bot:
            functions = []
            for name in function_names:
                functions.append(BotFunctions.objects.get(func_name=name))
            with open("first/botTelegram/start_template.py", 'r') as start_file:
                bot.write(start_file.read())
            for func in functions:
                print(func.file_name)
                with open(f'first/botTelegram/{func.file_name}', 'r') as file:
                    code = file.read()
                    bot.write(code)
            with open("first/botTelegram/end_template.py", 'r') as end_file:
                bot.write(end_file.read())
        with open('first/botTelegram/config.json', 'w') as json_file:
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
    return render(request, "tech_support.html", context)

