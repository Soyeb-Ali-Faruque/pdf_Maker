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
    #Admin
    path('admin/', admin.site.urls,name='admin'),

    #Home
    path('',views.home_view,name='home'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('otp_verification/', views.otp_view, name='signup_otp'),
    path('forget_password/', views.forget_password_view, name='forget_password'),
    path('forget_password_OTP/', views.forget_otp_view, name='forget_otp'),

    # User account operations
    path('user_profile/', views.profile_view, name='profile'),
    path('profile_picture_update/', views.update_picture_view, name='update_picture'),
    path('profile_picture_remove/', views.remove_picture_view, name='remove_picture'),
    path('update_name/', views.update_name_view, name='update_name'),
    path('update_username/', views.update_username_view, name='update_username'),
    path('delete_account/', views.delete_account_view, name='delete_account'),
    path('user_history/', views.user_history_view, name='user_history'),

    # File conversion(work need to be finished)
    path('text_to_pdf/', views.text_to_pdf_view, name='text_to_pdf'),
    path('html_to_pdf/', views.html_to_pdf_view, name='html_to_pdf'),
    path('image_to_pdf/', views.img_to_pdf_view, name='image_to_pdf'),
    path('docx_to_pdf/',views.docx_to_pdf_view,name='docx_to_pdf'),
    path('excel_to_pdf/', views.excel_to_pdf_view, name='excel_to_pdf'),
    path('powerpoint_to_pdf/',views.powerpoint_to_pdf_view,name='powerpoint_to_pdf'),
    path('texts_to_pdf/', views.texts_to_pdf_view, name='texts_to_pdf'),
    path('htmls_to_pdf/', views.htmls_to_pdf_view, name='htmls_to_pdf'),
    path('images_to_pdf/', views.imgs_to_pdf_view, name= 'images_to_pdf'),
    path('docxs_to_pdf/',views.docxs_to_pdf_view,name='docxs_to_pdf'),
    path('excels_to_pdf/', views.excels_to_pdf_view, name='excels_to_pdf'),
    path('powerpoints_to_pdf/',views.powerpoints_to_pdf_view,name='powerpoints_to_pdf'),
    path('multi_formats_to_pdf/',views.multi_formats_to_pdf_view,name='multi_formats_to_pdf'),


    # Feedback and policy
    path('feedback/', views.feedback_view, name='feedback'),
    path('privacy_policy/',views.privacy_policy_view,name='privacy_policy'),
    path('terms_and_conditions/',views.terms_and_conditions_view,name='terms_and_conditions'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)