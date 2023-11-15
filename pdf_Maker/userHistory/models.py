from django.db import models
from userlogin.models import userdata
# Create your models here.
class pdf_history(models.Model):
    file_name=models.CharField(max_length=121)
    file=models.FileField(upload_to="user_file/",null=True,default=None)
    pdf_file=models.FileField(upload_to="pdf",null=True,default=None)
    time=models.DateTimeField()
    user_info=models.ForeignKey(userdata,on_delete=models.CASCADE)
    

