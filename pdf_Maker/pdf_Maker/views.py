#PYTHON MODULE
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
from django.core.files.base import ContentFile
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




#--------------------------------home page--------------------------------------------------#

def home_view(request):
    
    return render(request,'index.html')
  

#-----------------user login and sign up and forget login credential-------------------------#

def login_view(request):
    message_password_updated=request.GET.get('passwordUpdated',False)
    message_acc_created=request.GET.get('acc_created',False)
    if request.method == 'POST':
        id=request.POST.get('id')
        password=request.POST.get('pass')
       
        try:
            user=userdata.objects.get(email=id)
        except userdata.DoesNotExist:
            try:
                user=userdata.objects.get(username=id)
            except userdata.DoesNotExist:
                user=None
        if user is not None and check_password(password,user.password):
                
            request.session['user_id'] = user.id
            
            return redirect('home')
        else:
                
            return render(request,'login.html',{'error':True})
     
    return render(request,'login.html',{'pass_updated':message_password_updated,'acc_created':message_acc_created})
def logout_view(request):
    request.session.pop('user_id',None)
    return redirect('home')
def signup_view(request):
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
            's5tech.sendmail@gmail.com',[email],
             fail_silently=False,
          )
        
       
        
        return redirect('signup_otp')
    return render(request,'login.html')
def otp_view(request):
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
                's5tech.sendmail@gmail.com',[email],
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
def forget_password_view(request):
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
                's5tech.sendmail@gmail.com', [email],
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
def forget_otp_view(request):
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
def get_user(request):
    user_id=request.session.get('user_id')
    user=userdata.objects.get(pk=user_id)
    return user 
def profile_view(request):
    error=request.GET.get('errorOccurr',None)
    return render(request,'profile.html',{'error':error})
def update_picture_view(request):
    user=get_user(request)
    if request.method=='POST':
        if user.profile_picture:
            
            path_to_delete = str(user.profile_picture)
            if os.path.exists(path_to_delete):
                os.remove(path_to_delete)
        
        picture=request.FILES.get('profile_picture')
        user.profile_picture=picture
        user.save()
        
    return redirect('profile')
def remove_picture_view(request):
    user=get_user(request)
    if request.method=='POST':
        if user.profile_picture:
            path_to_delete = str(user.profile_picture)
            if os.path.exists(path_to_delete):
                os.remove(path_to_delete)
            user.profile_picture=None
            user.save()
    return redirect('profile')
def update_name_view(request):
    user=get_user(request)
    if request.method == 'POST':
        get_name=request.POST.get('name')
        if len(get_name) < 5:
            messages.error(request, 'Please enter atlease 5 characters.')
    
        else:
            user.name=get_name
            user.save()
    return redirect(reverse('profile') + f'?errorOccurr=name')
def update_username_view(request):
    user=get_user(request)
    if request.method == 'POST':
        get_username=request.POST.get('username')
        if len(get_username) < 5:
            messages.error(request, 'Please enter atlease 5 characters.')
            return redirect(reverse('profile') + f'?errorOccurr=username')  
        
        elif ' ' in get_username:
            messages.error(request, 'Username should not contain any spaces.')
            return redirect(reverse('profile') + f'?errorOccurr=username') 
    
        else:
            user.username=get_username
            user.save()
            
    
    return redirect('profile')
def delete_account_view(request):
    user=get_user(request)
    if request.method=='POST':
        password=request.POST.get('password')
        if user is not None and check_password(password,user.password):
            user.delete()           
            return redirect('logout')
            
        else:
            return render(request,'delete_account.html',{'userPassword':True})
    return render(request,'delete_account.html')
def user_history_view(request):
    user_id = request.session.get('user_id', None)
    if user_id is not None:
        user_files = UserFile.objects.filter(user_id=user_id)
        return render(request, 'user_history.html', {'user_files': user_files})
    
    return render(request,'user_history.html')


#-----------------------------file conversion-----------------------------------------#

def isActive(request):
    user = request.session.get('user_id', None)
    if user is not None:
        return True
    return False
def store_user_history(request, user_filename, user_file_content, pdf_filename, pdf_content):
    user_id=request.session.get('user_id')
    if user_id:
        user=userdata.objects.get(pk=user_id)
        user_file=ContentFile(user_file_content.getvalue(),name=user_filename)
        pdf_file=ContentFile(pdf_content,name=pdf_filename)
        UserFile.objects.create(
            user=user,
            user_file=user_file,
            pdf_file=pdf_file
        )
     
def text_to_pdf_view(request):
    if request.method == 'POST':
        user_file = request.FILES.get('file')
        user_filename=user_file.name
        user_file_content = BytesIO()
        for chunk in user_file.chunks():
            user_file_content.write(chunk)
        
        if user_file:
            size_limit_kb = 600
            size_limit_bytes = size_limit_kb * 1024

            if user_file.size > size_limit_bytes:
                return render(request, 'pdf.html', {'file_accept': '.txt', 'file_size_exceeded': True})

            pdf_content = convert_text_to_pdf(user_file)
            pdf_filename=user_file.name.replace('.txt','.pdf')
           

            if isActive(request):
                store_user_history(request,user_filename,user_file_content,pdf_filename,pdf_content)

            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{user_file.name.replace(".txt", ".pdf")}"'
            return response

    return render(request, 'file_converter.html', {'file_accept': '.txt'})
def convert_text_to_pdf(file):
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)    
    styles = getSampleStyleSheet()    
    story = []

    # Debug print to verify file name
    print("File Name:", file.name)

    if file.name.endswith('.txt'):
        with file.open(mode='r') as txt_content:
            for line in txt_content:
                story.append(Paragraph(line, styles['Normal']))       
    pdf.build(story)

    # Set buffer position for reading
    pdf_buffer.seek(0)

    # Debug print to verify buffer size
    print("Buffer Size:", pdf_buffer.getbuffer().nbytes)

    return pdf_buffer.getvalue()
def img_to_pdf_view(request):
    if request.method == 'POST':
        user_file = request.FILES.get('file')
        if user_file:
            user_filename = user_file.name
            user_file_content = BytesIO()
            for chunk in user_file.chunks():
                user_file_content.write(chunk)
            
            pdf_filename = user_filename.replace('.png', '.pdf').replace('.jpg', '.pdf').replace('.jpeg', '.pdf')
            pdf_content = convert_image_to_pdf(user_file)
            
            if isActive(request) == True:
                store_user_history(request, user_filename, user_file_content, pdf_filename, pdf_content)

            
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response
    return render(request, 'file_converter.html', {'file_accept': '.png, .jpg, .jpeg'})
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
def compress_image_view(request):
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

    return render(request, 'compress_file.html', {'file_type': '.png, .jpg, .jpeg'})
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
def compress_pdf_view(request):
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
    return render(request,'compress_file.html',{'file_type':'.pdf'})


 #Feedback



#----------------------------Feedback------------------------------------------#

def feedback_view(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        print('name')
        email=request.POST.get('email')
       
        APP='PDF_Maker'
        admin_gmail='feedback.s5tech@gmail.com'
        feedback=request.POST.get('feedback')
        message=request.POST.get('message')
        
        send_mail(
            '{}-feedback'.format(APP),
            'Name: {}\n\nEmail:{}\n\nfeedback_type: {}\nSubject\n\n\{}'.format(name,email,feedback,message),
            's5tech.sendmail@gmail.com',
            [admin_gmail],
            fail_silently=False,
           
            
        )
        return redirect('home')
    return render(request,'feedback.html')