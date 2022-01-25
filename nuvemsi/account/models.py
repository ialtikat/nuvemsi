from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=80, default="")
    mail = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=11, default="")
    password = models.CharField(max_length=70, default="")
    key = models.CharField(max_length=100, default="")
    
class KeyUser(models.Model):
    user_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=11)
    key = models.CharField(max_length=256)