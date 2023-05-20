import datetime
import json
import os
import shutil
import smtplib
from distutils.dir_util import copy_tree
from email.mime.text import MIMEText
from dj_project.tasks import generate_bot, send_email

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


from first.models import BotFunctions, BotPreSets, FuncForPresets


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

                    result = generate_bot.delay(short_name, function_names, file_names, token, bot_os, request.user.name)
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
            result = generate_bot.delay(bot_name, function_names, file_names, bot_preset.token, bot_preset.os, request.user.name)
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

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
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
            _ = send_email.delay(message, user_email)

    return render(request, "tech_support.html", context)
