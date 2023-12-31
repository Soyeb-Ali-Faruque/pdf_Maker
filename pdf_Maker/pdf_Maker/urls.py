"""
URL configuration for pdf_Maker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pdf_Maker import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='Home'),
    path('login/',views.loginto,name='Login'),
    path('logout/',views.logout,name='Logout'),
    path('signup/',views.signup,name='Signup'),
    path('otp-verification',views.otp,name='Signup-otp'),
    path('forget-password/',views.forgetpass,name='Forget-password'),   
    path('forget-password-OTP/',views.forget_otp,name='Forget-otp'), 
    path('user-profile/',views.profile,name='Profile'),
    path('profile-picture-update',views.update_picture,name='Update-picture'),
    path('profile-picture-remove',views.remove_picture,name='Remove-picture'),
    path('delete-account/',views.delete_account,name='Delete-account'),
    path('txt_to-pdf',views.txtToPdf,name='txt'),
    
    
    
    
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
