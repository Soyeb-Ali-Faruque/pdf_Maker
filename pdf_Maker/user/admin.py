from django.contrib import admin
from user.models import UserInformation,UserFileHistory

# Register your models here.
admin.site.register(UserInformation)
admin.site.register(UserFileHistory)