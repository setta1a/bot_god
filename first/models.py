from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class BotFunctions(models.Model):
    func_name = models.CharField(max_length=64)
    file_name = models.CharField(max_length=64)

class UsersBalance(models.Model):
    balance = models.IntegerField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=2)
