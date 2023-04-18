import json
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from first.models import BotFunctions


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


@login_required(login_url='/login/')
def profile(request, profile_id):
    """
        Страница профиля пользователя

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    profile = User.objects.get(id=profile_id)
    context["profile"] = profile
    context["profile"] = User.objects.get(id=profile_id)
    return render(request, "profile.html", context)


@login_required(login_url='/login/')
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


def registration(request):
    """
        Обработчик страницы регистрации

        :param request: объект с деталями HTTP-запроса
        :return: Объект с деталями HTTP-ответа
    """
    context = {}
    context["pagetitle"] = "Registration"
    context["pageheader"] = "Регистрация"
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            context['form'] = form
            messages.add_message(request, messages.SUCCESS, "Новый пользователь создан")
        else:
            form = UserCreationForm()
            context['form'] = form
            messages.add_message(request, messages.ERROR, "Введены некорректные данные")
    else:
        form = UserCreationForm()
        context['form'] = form
    return render(request, 'registration/registration.html', context)


def tech_support(request):
    context = {}
    return render(request, "tech_support.html", context)


def create_file():
    with open('example.json', 'r') as f:
        data = json.loads(f.read())
        for i in data['employees']['employee']:
            if i['id'] == '3':
                print(i['photo'])
