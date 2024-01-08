from django.db import models

# Create your models here.
class Follow_Me(models.Model):
    image = models.ImageField(upload_to='admin_content/', null=True, default=None)
    name = models.CharField(max_length=255)
    link = models.URLField()
    
class ContactInformation(models.Model):
    contact_way = models.CharField(max_length=50)
    contact_details = models.CharField(max_length=255)
