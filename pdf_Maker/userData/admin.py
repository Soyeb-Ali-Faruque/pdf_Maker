from django.contrib import admin
from userData.models import userdata,UserFile

# Register your models here.
admin.site.register(userdata)
admin.site.register(UserFile)