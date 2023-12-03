from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

#used for login system
from django.contrib.auth.hashers import make_password, check_password
from userData.models import userdata,UserFile
from django.core.mail import send_mail
import random


#used for different file to pdf generation
from reportlab.pdfgen import canvas
from io import BytesIO


def home(request):
    user_id = request.session.get('user_id')
    user_information=None
    try:
        user_information=userdata.objects.get(pk=user_id)
        print(user_information)
    except Exception:
        
        return render(request,'index.html')
    return render(request,'index.html',{'user': user_information})
  

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
            data={'user':user}
            return render(request,'index.html',data)
        else:
                
            return render(request,'login.html',{'error':True})
     
    return render(request,'login.html',{'pass_updated':message_password_updated,'acc_created':message_acc_created})


def logout(request):
    request.session.pop('user_id',None)
    return redirect('/')

# this code is for sign up
#------------------sign up-------------------------------#
data_login={}
def signup(request):
    if request.method =='POST':
        email=request.POST.get('uemail')
        name=request.POST.get('uname')
        sendPassword=request.POST.get('upass')
        password=make_password(sendPassword)
        
        #username creation
        username=""
        for char in email:
            if char == '@':
                break
            username+=char
        
        user=userdata(email=email,password=password,name=name,userName=username)
        otpValue=""
        for i in range(0,6):
            otpValue+=str(random.randrange(0,9))
        send_mail(
            'otp-verification','your otp is {}'.format(otpValue),
            'sohebfaruque@gmail.com',[email],
            fail_silently=False
        )
        data_login['otp']=otpValue
        data_login['user']=user
        data_login['usermail']=email
        data_login['username']=username
        data_login['userPassword']=sendPassword
        
        return redirect('/otp-verification')
    return render(request,'login.html')
def otp(request):
 
    if request.method =='POST':
        user_otp=request.POST.get('otp')
        if user_otp == data_login['otp']:
            user=data_login['user']
            user.save()
            try:
                send_mail(
                'your login credential','your username is {} and password is {}'.format(data_login['username'],data_login['userPassword']),
                'sohebfaruque@gmail.com',[data_login[usermail]],
                fail_silently=False
                )
            except Exception:
                pass
            url='/login/?acc_created=True'
            return redirect(url)

        
        else:
            return render(request,'otp.html',{'incorrect':True})
    return render(request,'otp.html')       
  
#---------------sign up------------------------#




# forget password otp  generation
forgetPassword={'otp':'',
                'user_data':'',
                'setpassword':''}
def forgetpass(request):
    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        repassword=request.POST.get('repassword')
        try:
            user_data=userdata.objects.get(email=email)
        
            if password != repassword:
                return render(request,'forgetpass.html',{'incorrectPassword':True,'email':email})
            otpValue=""
            for i in range(0,6):
                otpValue+=str(random.randrange(0,9))
            
            forgetPassword['otp']=otpValue
            forgetPassword['user_data']=user_data
            forgetPassword['setpassword']=make_password(password)
            send_mail(
                'otp-reset your password','your otp is {}'.format(otpValue),
                'sohebfaruque@gmail.com',[email],
                fail_silently=False
            )
            return redirect('/forget-password-OTP')
        except:
            return render(request,'forgetpass.html',{'wrongEmail':True})
    return render(request,'forgetpass.html')

def forget_otp(request):
    if request.method == 'POST':
        otp=request.POST.get('otp')
        if otp == forgetPassword['otp']:
            user=forgetPassword['user_data']
            updated_password=forgetPassword['setpassword']
            user.password=updated_password
            user.save()
            
            url='/login/?passwordUpdated=True'
            return redirect(url)
        else:
            return render(request,'otp.html',{'incorrect':True})
            
    return render(request,'otp.html')

#user profile
def profile(request):
    user_id=request.session.get('user_id')
    user_information=None
    
    if user_id:
        try:
            user_information=userdata.objects.get(pk=user_id)
            return render(request,'profile.html',{'user':user_information})
        except userdata.DoesNotExist:
            return redirect('Login')
    return render(request,'login.html')

def update_picture(request):
    user_id=request.session.get('user_id')
    user=userdata.objects.get(pk=user_id)
    if request.method=='POST':
        picture=request.FILES.get('profile_picture')
        user.profile_picture=picture
        user.save()
        
    return redirect('Profile')

def remove_picture(request):
    user_id=request.session.get('user_id')
    user=userdata.objects.get(pk=user_id)
    if request.method=='POST':
        user.profile_picture=None
        user.save()
    return redirect('Profile')
        
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

#generate pdf
def convertText_to_pdf(txt_content):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 100, txt_content)
    pdf.save()
    buffer.seek(0)
    return buffer

    
def txtToPdf(request):
    user_id=request.session.get('user_id')
    fileType="txt"
    if request.method == 'POST':
        txt_file = request.FILES.get('file')
        print('yess')
        

        # Check if the uploaded file has a '.txt' extension
        if txt_file and txt_file.name.lower().endswith('.txt'):
            user_instance=userdata.objects.get(pk=user_id)
            print('yess')
            user_file = UserFile(user=user_instance,user_file=txt_file,)
            user_file.save()

            # Convert TXT content to PDF
            print("File Content:", txt_file.read().decode('utf-8'))
            txt_file.seek(0)
            txt_content = txt_file.read().decode('utf-8')
            print(txt_content,"hi")
            pdf_response = convertText_to_pdf(txt_content)
            print('yess')
            # Save the generated PDF file in the UserFile model
            user_file.pdf_file.save('output.pdf', pdf_response)
            #return generated pdf to template
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="output.pdf"'
            response.write(pdf_response)

            return response

            
        else:
            error_message = 'Please upload a valid text file (with .txt extension).'
            return render(request, 'MakePDF.html',{'type':fileType,'isError':True,'message':error_message})
    return render(request,'MakePDF.html',{'type':fileType})
    


