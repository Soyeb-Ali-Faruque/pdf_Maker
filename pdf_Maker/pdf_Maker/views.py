import random


#SYSTEM 
import os
from django.conf import settings

#DJANGO MODULES
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password



#MODELS
from userData.models import userdata,UserFile




#FILE OPERATION MODULES
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph  
#Image as PlatypusImage






def home(request):
    
    return render(request,'index.html')
  

#-----------------user login and sign up and forget login credential-------------------------#

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
        send_mail(
            'otp-verification','your otp is {}'.format(otpValue),
            'sohebfaruque@gmail.com',[email],
             fail_silently=False,
          )
        
       
        
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
                'sohebfaruque@gmail.com',[email],
                fail_silently=False
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
def forgetpass(request):
    if request.method == 'POST':
        # Get form data from the template
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        try:
            # Attempt to retrieve user data based on the provided email
            user_data = userdata.objects.get(email=email)
            print(user_data.email)  # Debug print to check if the user data is retrieved correctly

            # Check if passwords match
            if password != repassword:
                return render(request, 'forgetpass.html', {'incorrectPassword': True, 'email': email})

            # Generate OTP for verification
            otpValue = ""
            for i in range(0, 6):
                otpValue += str(random.randrange(0, 9))

            # Store data in session for further verification
            request.session['email'] = email
            request.session['otp'] = otpValue
            request.session['password'] = make_password(password)

            # Sending mail to the user
            send_mail(
                'otp-reset your password', 
                'your otp is {}'.format(otpValue),
                'sohebfaruque@gmail.com', [email],
                fail_silently=False
            )

            # Redirect to OTP verification page
            return redirect('Forget-otp')
        except userdata.DoesNotExist:
            # User data doesn't exist for the provided email
            return render(request, 'forgetpass.html', {'wrongEmail': True})
        except Exception as e:
            # Handle exception (e.g., log error, display error message)
            print("An error occurred while sending email:", e)

    # Render the forgetpass.html template for GET requests
    return render(request, 'forgetpass.html')
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



#--------------------------user account operations------------------------------------------#

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
def user_history(request):
    return render(request,'userHistory.html')


#-----------------------------file conversion-----------------------------------------#

def isActive(request):
    user = request.session.get('user_id', None)
    print("user primary key",user)
    if user is not None:
        return True
    return False
def store_user_history(request, user_file, pdf_content):
    user_id = request.session.get('user_id')
    if user_id:
        user_data = userdata.objects.get(pk=user_id)
        # Create a new entry in UserFile table
        user_history = UserFile.objects.create(
            user=user_data,
            user_file=user_file,
            
        )
        user_history.save()
def textToPdf(request):
    if request.method == 'POST':
        user_file=request.FILES.get('file')
        file=user_file
        if user_file:
            # Set the file size limit (600 KB)
            size_limit_kb = 600
            size_limit_bytes = size_limit_kb * 1024

            # Check the file size(in bytes)
            if user_file.size > size_limit_bytes:
                return render(request,'pdf.html',{'file_accept':'.txt','file_size_exceeded':True})
           
           
            pdf_content = convert_text_to_pdf(user_file)
            print(isActive(request))
            if isActive(request) == True:
                store_user_history(request,file,pdf_content)
                
            

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
    return pdf_buffer.getvalue()
def imgToPdf(request):
    if request.method == 'POST':
        user_file=request.FILES.get('file')
        pdf_content = convert_image_to_pdf(user_file)
        if isActive == True:
                store_user_history(user_file,pdf_content)

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
    return pdf_buffer.getvalue()
def compressImage(request):
    if request.method == 'POST':
        image_file = request.FILES.get('file')
        
        target_size= int(request.POST.get('target_size')) 
        unit=request.POST.get('unit')
        
        if unit == 'MB':
            # converting the mb to kb
            target_size= target_size * 1024

        
        # Call the function for compression
        compressed_img = compress_image(image_file, target_size)
        
        # Prepare response
        response = HttpResponse(compressed_img.getvalue(), content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename="compressed_image.jpg"'
        return response

    return render(request, 'CompressFILE.html', {'file_type': '.png, .jpg, .jpeg'})
def compress_image(file, target_size_kb=300):
    img = Image.open(file)
    original_size = img.size[0] * img.size[1] * 3  
    
    
    # Initialize quality parameters
    min_quality = 0
    max_quality = 100
    quality = (min_quality + max_quality) // 2 
    
    # Compress the image using binary search
    while True:
        # Compress the image
        compressed_img = BytesIO()
        img.save(compressed_img, format='JPEG', quality=quality)
        
        # Get the size of the compressed image
        compressed_size = len(compressed_img.getvalue())
        
        
        # Check if the compressed size is within the target range
        if compressed_size <= target_size_kb * 1024:
            break  # If compressed size is within target, break the loop
        else:
            # Adjust quality based on binary search
            if compressed_size > target_size_kb * 1024:
                max_quality = quality - 1
            else:
                min_quality = quality + 1
            
            # Check if quality becomes too low or too high
            if min_quality > max_quality:
                # Compression quality too low, break the loop
                break
            
            # Update quality for next iteration
            quality = (min_quality + max_quality) // 2
    
    return compressed_img
def compressPdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES['file']
        target_size= int(request.POST.get('target_size')) 
        unit=request.POST.get('unit')
        
        if unit == 'MB':
            # converting the mb to kb
            target_size *= 1024
        
        # Call the function for compression
        compressed_pdf = compress_pdf(pdf_file,target_size)
        
        # Prepare response
        response = HttpResponse(compressed_pdf.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="compressed_pdf.pdf"'
        return response
    return render(request,'CompressFILE.html',{'file_type':'.pdf'})


 #Feedback



#----------------------------------------------------------------------#

def feedback(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        print('name')
        email=request.POST.get('email')
        print(gmail)
        APP='PDF_Maker'
        admin_gmail='feedback.s5tech@gmail.com'
        feedback=request.POST.get('feedback')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        
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