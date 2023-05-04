from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class BotFunctions(models.Model):
    func_name = models.CharField(max_length=64)
    file_name = models.CharField(max_length=64)

class BotPreSets(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    bot_name = models.CharField(max_length=32)
    created_at = models.DateTimeField()
    token = models.CharField(max_length=64)
    os = models.CharField(max_length=4)

class FuncForPresets(models.Model):
    func = models.ForeignKey(to=BotFunctions, on_delete=models.CASCADE)
    bot = models.ForeignKey(to=BotPreSets, on_delete=models.CASCADE)

