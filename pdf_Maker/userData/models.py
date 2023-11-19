from django.db import models
from django.utils import timezone

# Create your models here.
class userdata(models.Model):
    name=models.CharField(max_length=100,null=True)
    userName=models.CharField(max_length=121,null=True,default="Defaultusername")
    email=models.EmailField()
    password=models.CharField(max_length=290)
    profile_picture=models.FileField(upload_to="user_profile/", null=True, default=None)
