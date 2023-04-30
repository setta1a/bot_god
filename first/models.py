from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class BotFunctions(models.Model):
    func_name = models.CharField(max_length=64)
    file_name = models.CharField(max_length=64)

class BotPreSets(models.Model):
    file_name = models.CharField(max_length=64)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    bot_name = models.CharField(max_length=32)
    created_at = models.DateTimeField()

