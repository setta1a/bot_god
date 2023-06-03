import datetime
import json
import os
import shutil
import smtplib
from distutils.dir_util import copy_tree
from email.mime.text import MIMEText
from functionClass import BotFunction
from django.http import JsonResponse

from dj_project.tasks import generate_bot, send_email

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from first.models import BotFunctions, BotPreSets, FuncForPresets


def api_check_bot(request):
    context = dict()
    if request.method == "GET" and request.GET.get("bot_name", "") != "":
        bot_name = request.GET['bot_name']
        cnt = BotPreSets.objects.filter(bot_name=bot_name).count()
        res = (cnt != 0)
        context['has_bot'] = res
    return JsonResponse(context)


def index(request):
    """
        Главная страница

        :param request: объект с деталями HTTP-запроса
        :return: **context** - объект с деталями HTTP-ответа (пустой)
    """
    context = {}
    if request.method == "GET":
        print(request.GET)
    return render(request, "index.html", context)


def telegram_auth(request):
    context = {}
    return render(request, "telegram_auth.html", context)


def create_bot(request):
    """
        Страница создания бота

        :param request: объект с деталями HTTP-запроса
        :return: **context** - объект с деталями HTTP-ответа (пустой)
        :return: **redirect** - перекидование на страницу оплаты
    """
    context = {}
    context['bot_functions'] = []
    for filename in os.listdir(os.getcwd() + '/functions_info'):
        with open(os.path.join(os.getcwd() + '/functions_info', filename), 'r') as f:
            fields = f.readlines()
            os_availability = list(map(int, fields[3].split()))
            context['bot_functions'].append(BotFunction(fields[0], fields[1], fields[2], os_availability, fields[4], fields[5], fields[6]))

    if request.method == "POST":
        if 'functions' in request.POST and 'os' in request.POST and 'short_name' in request.POST and 'token' in request.POST and 'name' in request.POST:
            function_names = request.POST.getlist('functions')
            short_name = request.POST['short_name']
            token = request.POST['token']
            bot_os = request.POST['os']
            file_names = []
            functions = []
            for name in function_names:
                bot_function = BotFunctions.objects.get(func_name=name)
                functions.append(bot_function)
                file_names.append(bot_function.file_name)

            if request.user.is_authenticated:
                filterargs = {'bot_name': request.POST['short_name'], 'user': request.user}
                if BotPreSets.objects.filter(**filterargs).count() == 0:
                    bot_preset = BotPreSets(user=request.user, bot_name=request.POST['short_name'],
                                            created_at=datetime.datetime.now(), token=request.POST['token'],
                                            os=request.POST['os'])
                    bot_preset.save()

                    for function in functions:
                        function_preset = FuncForPresets(func_name=function, bot=bot_preset)
                        function_preset.save()

                    _ = generate_bot.delay(short_name, function_names, file_names, token, bot_os,
                                                request.user.username)
                    return redirect(f"../download_bot/?os={bot_os}&file={short_name}")


    return render(request, "create_bot.html", context)


def download_bot(request):
    context = {}
    if request.method == "GET":
        if "file" in request.GET and 'os' in request.GET:
            context['os'] = request.GET['os']
            context['file'] = request.GET['file']
        else:
            bot_name = request.GET['preset']
            bot_preset = BotPreSets.objects.get(bot_name=bot_name)
            functions = FuncForPresets.objects.filter(bot=bot_preset)
            function_names = []
            file_names = []

            for function in functions:
                file_names.append(function.func_name.file_name)
                function_names.append(function.func_name.func_name)

            context['file'] = bot_name
            context['os'] = bot_preset.os
            context['bot_status'] = ""
            result = generate_bot.delay(bot_name, function_names, file_names, bot_preset.token, bot_preset.os,
                                        request.user.username)
            context['bot_status'] = str(result.state)
            if (str(result.state) != "SUCCESS"):
                context['bot_status'] = ""
            else:
                context['bot_status'] = "SUCCESS"
                return render(request, "download_bot.html", context)

    return render(request, "download_bot.html", context)


@login_required(login_url='/telegram_auth/')
def profile(request):
    """
        Страница профиля пользователя

        :param request: объект с деталями HTTP-запроса, **id** пользователя
        :return: **context** - объект с деталями HTTP-ответа
    """
    context = {}
    if request.method == "POST":
        for name in request.POST:
            res = name.split()
            if res[0] == "delete_bot":
                bot_id = int(res[1])
                bot_delete = BotPreSets.objects.get(id=bot_id)
                bot_delete.delete()

    context['bots'] = BotPreSets.objects.filter(user=request.user)
    return render(request, "profile.html", context)


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
            result_message = f"Пользователь {user_email} отправил сообщение с текстом: {message} \n Ответьте ему как можно быстрее!"
            try:
                print(1)
                server.login(sender, password)
                msg = MIMEText(result_message)
                msg["Subject"] = "ЖАЛОБА ОТ ПОЛЬЗОВАТЕЛЯ"
                server.sendmail(sender, "andreysitalo09@gmail.com", msg.as_string())

                message = '''<!DOCTYPE html>
                                <html lang="en" style="font-size: 18px; margin: 0; padding: 0;">
                                <head>
                                    <meta charset="UTF-8">
                                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                    <title>Message</title>
                                </head>
                                <body style="margin: 0; padding: 0;">
                                    <header style="padding: 1%; margin: 0; color: white; background-color: #023653; margin-bottom: 5%;">
                                        <h1 style="margin: auto; text-align: center;">BOTGOD</h1>
                                    </header>
                                    <main style="width: 70%; margin: 0 auto; border: 2px solid #023653; border-radius: 30px; padding: 1%;">
                                        <article>Ваше сообщение очень важно для нас. Оно будет рассмотрено в ближайшее время и на вашу почту будет направлен ответ. С уважением, команда BotGod.</article>
                                    </main>
                                    <footer>

                                    </footer>
                                </body>
                                </html>
'''
                msg = MIMEText(message, 'html')
                msg["Subject"] = "ЖАЛОБА ОТ ПОЛЬЗОВАТЕЛЯ"
                server.sendmail(sender, user_email, msg.as_string())

            except Exception as _ex:
                print(f"{_ex}\nCheck your login or password please!")
    return render(request, "tech_support.html", context)
