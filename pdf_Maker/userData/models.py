from django.db import models


# Create your models here.
class userdata(models.Model):
    name=models.CharField(max_length=100,null=True)
    userName=models.CharField(max_length=121,null=True,default="Defaultusername")
    email=models.EmailField()
    password=models.CharField(max_length=290)
    profile_picture=models.FileField(upload_to="user/user_profile/", null=True, default=None)

class UserFile(models.Model):
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)
    user_file = models.FileField(upload_to="user/user_files/",null=True, default=None)
    pdf_file = models.FileField(upload_to="user/pdf_files/",null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
