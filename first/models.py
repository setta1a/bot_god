from django.db import models
from social_django.models import UserSocialAuth
# Create your models here.
class BotFunctions(models.Model):
    func_name = models.CharField(max_length=64)
    file_name = models.CharField(max_length=64)


class UsersBalance(models.Model):
    balance = models.IntegerField()
    user = models.ForeignKey(to=UserSocialAuth, on_delete=models.CASCADE)
