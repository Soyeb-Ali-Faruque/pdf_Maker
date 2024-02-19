import os
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib import messages
from django.urls import reverse


#used for login system
from django.contrib.auth.hashers import make_password, check_password
from userData.models import userdata,UserFile
from django.core.mail import send_mail,EmailMessage, get_connection
import random







#used for different file to pdf generation
from reportlab.lib import utils
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph,  Image as PlatypusImage







def home(request):
    return render(request,'index.html')
  

def loginto(request):
    message_password_updated=request.GET.get('passwordUpdated',False)
    message_acc_created=request.GET.get('acc_created',False)
    if request.method == 'POST':
        id=request.POST.get('id')
        password=request.POST.get('pass')
       
        try:
            user=userdata.objects.get(email=id)
        except userdata.DoesNotExist:
            try:
                user=userdata.objects.get(userName=id)
            except userdata.DoesNotExist:
                user=None
        if user is not None and check_password(password,user.password):
                
            request.session['user_id'] = user.id
            
            return redirect('Home')
        else:
                
            return render(request,'login.html',{'error':True})
     
    return render(request,'login.html',{'pass_updated':message_password_updated,'acc_created':message_acc_created})


def logout(request):
    request.session.pop('user_id',None)
    return redirect('/')

# this code is for sign up
#------------------sign up-------------------------------#

def signup(request):
    if request.method =='POST':
        email=request.POST.get('uemail')
        #condition for checking if the account is already made by this email or not 
        hasAccount=userdata.objects.filter(email=email).first()
        if hasAccount is not None:
            return render(request,'login.html',{'error_alreadyAccountExist':True,'email':email})
        
        name=request.POST.get('uname')
        password=request.POST.get('upass')
       # password=make_password(sendPassword)
        
        #username creation
        username=""
        for char in email:
            if char == '@':
                break
            username+=char
        
        #
        otpValue=""
        for i in range(0,6):
            otpValue+=str(random.randrange(0,9))
        
        #session data storation
        request.session['username']=username
        request.session['password']=password
        request.session['name']=name
        request.session['email']=email
        request.session['otp']=otpValue
        
       
       #sending otp to the associated mail
        email_message = EmailMessage(
           'otp-verification',
            'Your OTP is {}'.format(otpValue),
            'otp.automailer@gmail.com',
            [email],
            connection=get_connection(settings.EMAIL_BACKEND_1),
        )
        email_message.send(fail_silently=False)
       
        
        return redirect('Signup-otp')
    return render(request,'login.html')
def otp(request):
    name=request.session.get('name')
    username=request.session.get('username')
    password=make_password(request.session.get('password'))
    email=request.session.get('email')
    otp=request.session.get('otp')
    
 
    if request.method =='POST':
        user_otp=request.POST.get('otp')
        if user_otp == otp:
            
            user=userdata(email=email,password=password,name=name,userName=username)
            user.save()
           
           
           #sending username password
            send_mail(
                'your login credential','your username is {} and password is {}'.format(username,request.session.get('password')),
                settings.EMAIL_HOST_USER_2,[email],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER_2,
                auth_password=settings.EMAIL_HOST_PASSWORD_2,
                connection_kwargs={
                    'host': settings.EMAIL_HOST_2,
                    'port': settings.EMAIL_PORT_2,
                    'use_tls': settings.EMAIL_USE_TLS_2,
                },
                
                )
            
            #pop or remove information from session
            request.session.pop('name',None)
            request.session.pop('username',None)
            request.session.pop('password',None)
            request.session.pop('email',None)
            request.session.pop('otp',None)
            
            url='/login/?acc_created=True'
            return redirect(url)

        
        else:
            return render(request,'otp.html',{'incorrect':True})
    return render(request,'otp.html')       
  
#---------------sign up------------------------#




# forget password otp  generation
def forgetpass(request):
    if request.method =='POST':
        #get form data from template
        email=request.POST.get('email')
        password=request.POST.get('password')
        repassword=request.POST.get('repassword')
        
        
        try:
            user_data=userdata.objects.get(email=email)
        
            if password != repassword:
                return render(request,'forgetpass.html',{'incorrectPassword':True,'email':email})
        
        #generate otp for verification
            otpValue=""
            for i in range(0,6):
                otpValue+=str(random.randrange(0,9))
        
            request.session['email']=email    
            request.session['otp']=otpValue           
            request.session['password']=make_password(password)          
        
        
        #sending mail to the user
            send_mail(
                'otp-reset your password','your otp is {}'.format(otpValue),
                settings.EMAIL_HOST_USER_1,[email],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER_1,
                auth_password=settings.EMAIL_HOST_PASSWORD_1,
                connection_kwargs={
                     'host': settings.EMAIL_HOST_1,
                    'port': settings.EMAIL_PORT_1,
                     'use_tls': settings.EMAIL_USE_TLS_1,
                 },
            )
            return redirect('/forget-password-OTP')
        except:
            return render(request,'forgetpass.html',{'wrongEmail':True})
    return render(request,'forgetpass.html')

def forget_otp(request):
    if request.method == 'POST':
        otp_from_user=request.POST.get('otp')
        otp_Backend_storage=request.session.get('otp')
        if otp_from_user == otp_Backend_storage:
            email=request.session.get('email')
            user=userdata.objects.get(email=email)
            updated_password=request.session.get('password')
            user.password=updated_password
            user.save()
            request.session.pop('otp')
            request.session.pop('email')
            request.session.pop('password')
            
            url='/login/?passwordUpdated=True'
            return redirect(url)
        else:
            return render(request,'otp.html',{'incorrect':True})
            
    return render(request,'otp.html')

#user profile
def profile(request):
    error=request.GET.get('errorOccurr',None)
    return render(request,'profile.html',{'error':error})


def update_picture(request):
    user_id=request.session.get('user_id')
    user=userdata.objects.get(pk=user_id)
    if request.method=='POST':
        if user.profile_picture:
            
            path_to_delete = os.path.join(settings.MEDIA_ROOT, str(user.profile_picture))
            if os.path.exists(path_to_delete):
                os.remove(path_to_delete)
        
        picture=request.FILES.get('profile_picture')
        user.profile_picture=picture
        user.save()
        
    return redirect('Profile')

def remove_picture(request):
    user_id=request.session.get('user_id')
    user=userdata.objects.get(pk=user_id)
    if request.method=='POST':
        if user.profile_picture:
            path_to_delete = os.path.join(settings.MEDIA_ROOT, str(user.profile_picture))
            if os.path.exists(path_to_delete):
                os.remove(path_to_delete)
            user.profile_picture=None
            user.save()
    return redirect('Profile')
def update_name(request):
    user_id=request.session.get('user_id')
    user=userdata.objects.get(pk=user_id)
    if request.method == 'POST':
        get_name=request.POST.get('name')
        if len(get_name) < 5:
            messages.error(request, 'Please enter atlease 5 characters.')
    
        else:
            user.name=get_name
            user.save()
    return redirect(reverse('Profile') + f'?errorOccurr=name')
def update_username(request):
    user_id=request.session.get('user_id')
    user=userdata.objects.get(pk=user_id)
    if request.method == 'POST':
        get_username=request.POST.get('username')
        if len(get_username) < 5:
            messages.error(request, 'Please enter atlease 5 characters.')
    
        else:
            user.username=get_username
            user.save()
    return redirect(reverse('Profile') + f'?errorOccurr=username')   
def delete_account(request):
    user_id=request.session.get('user_id')
    user=userdata.objects.get(pk=user_id)
    if request.method=='POST':
        password=request.POST.get('password')
        if user is not None and check_password(password,user.password):
            user.delete()
            
            return redirect('Logout')
            
        else:
            return render(request,'deleteAccount.html',{'userPassword':True})
    return render(request,'deleteAccount.html')

#pdf generations from different file__________________-___________________

# text to pdf
def textToPdf(request):
    if request.method == 'POST':
        user_file=request.FILES.get('file')
        if user_file:
            # Set the file size limit (600 KB)
            size_limit_kb = 600
            size_limit_bytes = size_limit_kb * 1024

            # Check the file size(in bytes)
            if user_file.size > size_limit_bytes:
                return render(request,'pdf.html',{'file_accept':'.txt','file_size_exceeded':True})
           
           
            pdf_content = convert_text_to_pdf(user_file)

            # Send the PDF to the frontend for automatic downloading
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{user_file.name.replace(".txt", ".pdf")}"'
            return response
    return render(request,'pdf.html',{'file_accept':'.txt'})

 
def convert_text_to_pdf(file):
    # Create a BytesIO buffer to store the PDF content
    pdf_buffer = BytesIO()

    # Create a PDF document using reportlab
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)    
    styles = getSampleStyleSheet()    
    story = []
    
    # text to PDF conversion
    if file.name.endswith('.txt'):
        with file.open(mode='r') as txt_content:
            for line in txt_content:
                story.append(Paragraph(line, styles['Normal']))       
    pdf.build(story)
    # Set the buffer position to the beginning for reading
    pdf_buffer.seek(0)
    # Return the filename for use in Content-Disposition header
    return pdf_buffer




#Image to pdf
def imgToPdf(request):
    if request.method == 'POST':
        user_file=request.FILES.get('file')
        pdf_content = convert_image_to_pdf(user_file)

        # Send the PDF to the frontend for automatic downloading
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{user_file.name.replace(".jpg", ".pdf").replace(".jpeg", ".pdf").replace(".png", ".pdf")}"'
        return response
        
    return render(request,'pdf.html',{'file_accept':'.png, .jpg, .jpeg'})

def convert_image_to_pdf(file):
    pdf_buffer = BytesIO()
     # Create a PDF document using reportlab
    pdf = canvas.Canvas(pdf_buffer)
    image = Image.open(file)
    image_reader = ImageReader(image)
    width, height = image.size
    if width > height:
        pdf.setPageSize((width, height))
        pdf.drawImage(image_reader, 0, 0, width, height)
    else:
        pdf.setPageSize(letter)
        pdf.drawImage(image_reader, 0, 0,width=595.276, height=841.890)
    
    
    pdf.save()
    # Set the buffer position to the beginning for reading
    pdf_buffer.seek(0)
    return pdf_buffer.read()



# Compress Files
def compressImage(request):
    return render(request,'CompressFILE.html',{'file_type':'.png, .jpg, .jpeg'})
def compressPdf(request):
    return render(request,'CompressFILE.html',{'file_type':'.pdf'})

 
 
 
  
#Feedback
def feedback(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        feedback=request.POST.get('feedback')
        send_mail(
            'PDF MAKER-feedback',
            'Name: {}\nfeedback: {}'.format(name,feedback),
            settings.EMAIL_HOST_USER_2,
            ['soyebali0101@gmail.com'],
            fail_silently=False,
            auth_user=settings.EMAIL_HOST_USER_2,
            auth_password=settings.EMAIL_HOST_PASSWORD_2,
            connection_kwargs={
              'host': settings.EMAIL_HOST_2,
              'port': settings.EMAIL_PORT_2,
              'use_tls': settings.EMAIL_USE_TLS_2,
        },
            
        )
        return redirect('Home')
    return render(request,'feedback.html')