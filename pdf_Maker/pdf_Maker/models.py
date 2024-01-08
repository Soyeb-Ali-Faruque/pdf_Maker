from django.db import models
class Follow_Me(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=255)
    link = models.URLField()
    
class ContactInformation(models.Model):
    contact_way = models.CharField(max_length=50)
    contact_details = models.CharField(max_length=255)