"""dj_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from operator import index
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from first.views import index, create_bot, payment, profile, redact_profile, tech_support, telegram_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index),
    path('create_bot/', create_bot),
    path('login/', auth_views.LoginView.as_view(
        extra_context={
            "pagetitle": "Auth",
            "pageheader": "Авторизация"
        }
    )),
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', auth_views.LogoutView.as_view()),
    path("payment/", payment),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('redact_profile/<int:redact_profile_id>', redact_profile),
    path("tech_support/", tech_support),
    path("telegram_auth/", TemplateView.as_view(template_name='telegram_auth.html'))
]
