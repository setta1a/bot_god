from django.db import models

# Create your models here.
class BotFunctions(models.Model):
    func_name = models.CharField(max_length=64)
    file_name = models.CharField(max_length=64)
