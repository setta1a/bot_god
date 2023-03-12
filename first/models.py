from django.db import models

# Create your models here.
class BotFunctions(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=1024)