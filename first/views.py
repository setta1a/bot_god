import datetime
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect


def index(request):
    context = {}
    return render(request, "index.html", context)


def create_bot(request):
    context = {}
    if request.method == "POST":
        return redirect("../payment/")
    return render(request, "create_bot.html", context)


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


# Create your views here.
