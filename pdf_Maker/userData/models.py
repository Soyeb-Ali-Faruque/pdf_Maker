from django.db import models
from django.utils import timezone

# Create your models here.
class userdata(models.Model):
    name=models.CharField(max_length=100,null=True)
    userName=models.CharField(max_length=121,null=True,default="Defaultusername")
    email=models.EmailField()
    password=models.CharField(max_length=290)
    profile_picture=models.FileField(upload_to="user_profile/", null=True, default=None)

class UserFile(models.Model):
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)
    user_file = models.FileField(upload_to="user_files/")
    pdf_file = models.FileField(upload_to="pdf_files/")
    created_at = models.DateTimeField(auto_now_add=True)
