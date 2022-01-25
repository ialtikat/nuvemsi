from django.db import models

# Create your models here.
class Uploadİmg(models.Model):
    imgname=models.ImageField(upload_to="ximages", max_length=100)
    size=models.CharField(max_length=10, default="")
    imgcode=models.TextField()
    username=models.CharField(max_length=80, default="")
    userid=models.CharField(max_length=5, default="")
    keyid=models.CharField(max_length=5, default="")
    
class UploadDoc(models.Model):
    docname=models.FileField(upload_to="ximages", max_length=100)
    size=models.CharField(max_length=10, default="")
    doccode=models.TextField()
    username=models.CharField(max_length=80, default="")
    userid=models.CharField(max_length=5, default="")
    keyid=models.CharField(max_length=5, default="")