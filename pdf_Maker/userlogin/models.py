from django.db import models

# Create your models here.
class userdata(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=290)
    
