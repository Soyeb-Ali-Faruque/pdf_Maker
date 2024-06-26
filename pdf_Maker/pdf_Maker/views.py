#PYTHON MODULE
import random


#SYSTEM
import os
import subprocess
from django.conf import settings
from tempfile import TemporaryDirectory

#DJANGO MODULES
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse,HttpResponseBadRequest
from django.utils.html import strip_tags
from django.shortcuts import render,redirect
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.auth.hashers import make_password, check_password

#MODELS
from user.models import UserInformation,UserFileHistory

#FILE OPERATION MODULES
import pdfkit
import img2pdf
from io import BytesIO
from PIL import Image, ExifTags
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

#--------------------------------home page--------------------------------------------------#

def home_view(request):

    return render(request,'index.html')

#-----------------user login and sign up and forget login credential-------------------------#

def otp_verification_mail(name,otpValue,validity,mail_to):
    context = {
         'user_name': name,
         'otp_code': otpValue,
          'valid_minutes': validity,
        }
    html_message = render_to_string('mail_otp_to_user.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'PDF Maker <s5tech.sendmail@gmail.com>'
    to = mail_to
    # Send the OTP email
    email_message = EmailMultiAlternatives(
        'Verify Your PDF Maker Account', plain_message, from_email, [to]
        )
    email_message.attach_alternative(html_message, "text/html")
    email_message.send()
def login_view(request):
    message_password_updated=request.GET.get('passwordUpdated',False)

    if request.method == 'POST':
        id=request.POST.get('id')
        password=request.POST.get('pass')

        try:
            user=UserInformation.objects.get(email=id)
        except UserInformation.DoesNotExist:
            try:
                user=UserInformation.objects.get(username=id)
            except UserInformation.DoesNotExist:
                user=None
        if user is not None and check_password(password,user.password):

            request.session['user_id'] = user.id

            return redirect('home')
        else:

            return render(request,'login.html',{'error':True})

    return render(request,'login.html',{'pass_updated':message_password_updated})
def logout_view(request):
    request.session.pop('user_id',None)
    return redirect('home')
def signup_view(request):
    if request.method =='POST':
        email=request.POST.get('uemail')

        #condition for checking if the account is already made by this email or not
        hasAccount=UserInformation.objects.filter(email=email).first()
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

        print("username from signup view  ",username)
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
       #---------------outdated------------------------#
        # send_mail(
        #     'otp-verification','your otp is {}'.format(otpValue),
        #     's5tech.sendmail@gmail.com',[email],
        #      fail_silently=False,
        #   )
        #----------------------------------------------#

        otp_verification_mail(name,otpValue,3,email)





        return redirect('signup_otp')
    return render(request,'login.html')
def otp_view(request):
    name=request.session.get('name')
    email=request.session.get('email')
    username=request.session.get('username')
    if email is not None and username is not None:
        email = email.lower()
        username = username.lower()
    password=make_password(request.session.get('password'))
    otp=request.session.get('otp')


    if request.method =='POST':
        user_otp=request.POST.get('otp')
        if user_otp == otp:

            user=UserInformation(email=email,password=password,name=name,username=username)
            user.save()
            request.session['user_id'] = user.id

            #pop or remove information from session
            request.session.pop('name',None)
            request.session.pop('username',None)
            request.session.pop('password',None)
            request.session.pop('email',None)
            request.session.pop('otp',None)



            return redirect('home')


        else:
            return render(request,'otp.html',{'incorrect':True})
    return render(request,'otp.html')
def forget_password_view(request):
    if request.method == 'POST':
        # Get form data from the template
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        print("before try")
        try:
            print("inner try")

            # Attempt to retrieve user data based on the provided email
            user_data = UserInformation.objects.get(email=email)
            print("after user object retrieve")
            # Generate OTP for verification
            otpValue = ""
            for i in range(0, 6):
                otpValue += str(random.randrange(0, 9))

            # Store data in session for further verification
            request.session['email'] = email
            request.session['otp'] = otpValue
            request.session['password'] = make_password(password)

            # Sending mail to the user
            # send_mail(
            #     'otp-reset your password',
            #     'your otp is {}'.format(otpValue),
            #     's5tech.sendmail@gmail.com', [email],
            #     fail_silently=False
            # )

            otp_verification_mail(user_data.name,otpValue,3,email)

            # Redirect to OTP verification page
            return redirect('forget_otp')
        except UserInformation.DoesNotExist:
            print("exeption")
            # User data doesn't exist for the provided email
            return render(request, 'forget_password.html', {'wrongEmail': True})
        except Exception as e:
            # Handle exception (e.g., log error, display error message)
            print("An error occurred while sending email:", e)

    # Render the forgetpass.html template for GET requests
    return render(request, 'forget_password.html')
def forget_otp_view(request):
    if request.method == 'POST':
        otp_from_user=request.POST.get('otp')
        otp_Backend_storage=request.session.get('otp')
        if otp_from_user == otp_Backend_storage:
            email=request.session.get('email')
            user=UserInformation.objects.get(email=email)
            updated_password=request.session.get('password')
            user.password=updated_password
            user.save()
            request.session['user_id'] = user.id
            request.session.pop('otp')
            request.session.pop('email')
            request.session.pop('password')


            return redirect('home')
        else:
            return render(request,'otp.html',{'incorrect':True})

    return render(request,'otp.html')

#--------------------------user account operations------------------------------------------#

def get_user(request):
    user_id=request.session.get('user_id')
    user=UserInformation.objects.get(pk=user_id)
    return user
def profile_view(request):
    error=request.GET.get('errorOccurr',None)
    return render(request,'profile.html',{'error':error})
def update_picture_view(request):
    user = get_user(request)
    if request.method == 'POST':
        if user.profile_picture:
            path_to_delete = os.path.join(settings.MEDIA_ROOT, str(user.profile_picture))
            if os.path.exists(path_to_delete):
                os.remove(path_to_delete)
        picture = request.FILES.get('profile_picture')
        if not picture.name.lower().endswith(('jpeg', 'png', 'jpg')):
            return HttpResponseBadRequest('Only JPEG, PNG, and JPG formats are allowed.')
        user.profile_picture = picture
        user.save()
    return redirect('profile')
def remove_picture_view(request):
    user=get_user(request)
    if request.method=='POST':
        if user.profile_picture:
            path_to_delete =os.path.join(settings.MEDIA_ROOT, str(user.profile_picture))
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
    user = get_user(request)
    if request.method == 'POST':
        get_username = request.POST.get('username')
        if len(get_username) < 5:
            messages.error(request, 'Please enter at least 5 characters.')
            return redirect(reverse('profile') + f'?errorOccurr=username')
        elif ' ' in get_username:
            messages.error(request, 'Username should not contain any spaces.')
            return redirect(reverse('profile') + f'?errorOccurr=username')
        elif UserInformation.objects.filter(username=get_username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect(reverse('profile') + f'?errorOccurr=username')
        else:
            user.username = get_username
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
        user_files = UserFileHistory.objects.filter(user_id=user_id)
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
        user=UserInformation.objects.get(pk=user_id)
        user_file=None
        if user_file_content is not None:
            user_file=ContentFile(user_file_content.getvalue(),name=user_filename)
        pdf_file=ContentFile(pdf_content,name=pdf_filename)
        UserFileHistory.objects.create(
            user=user,
            user_file=user_file,
            pdf_file=pdf_file
        )


#################### FIle conversion fucntions ##############################
def combine_pdfs(pdf_contents):
    combined_pdf = BytesIO()
    pdf_writer = PdfWriter()

    for pdf_content in pdf_contents:
        # Check if the content is bytes, if so, convert it to BytesIO
        if isinstance(pdf_content, bytes):
            pdf_content = BytesIO(pdf_content)

        # Ensure it's at the beginning
        pdf_content.seek(0)

        # Read the PDF content
        pdf_reader = PdfReader(pdf_content)

        # Add all pages of this PDF to the writer
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    # Write the combined PDF to the BytesIO object
    pdf_writer.write(combined_pdf)
    combined_pdf.seek(0)
    return combined_pdf.getvalue()
def convert_text_to_pdf(file):
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    file.seek(0)
    txt_content = file.read().decode('utf-8')
    for line in txt_content.splitlines():
        story.append(Paragraph(line, styles['Normal']))
    pdf.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()
def convert_html_to_pdf(html_file_content):
    pdf_file_content = pdfkit.from_string(html_file_content.read().decode('utf-8'), False)
    return pdf_file_content
def convert_image_to_pdf(image_file):
    """
    img2pdf.ExifOrientationError: Raised when img2pdf encounters invalid rotation
    information in the Exif metadata of the image.
    """

    image_file.seek(0)

    try:
        pdf_content = img2pdf.convert(image_file)
        return pdf_content
    except img2pdf.ExifOrientationError:
        image_file.seek(0)
        image = Image.open(image_file)
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(image._getexif().items())
            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            pass
        corrected_image_content = BytesIO()
        image.save(corrected_image_content, format=image.format)
        corrected_image_content.seek(0)
        pdf_content = img2pdf.convert(corrected_image_content)
        return pdf_content
def convert_docx_to_pdf(docx_content):
    with TemporaryDirectory() as temp_dir:
        docx_path = os.path.join(temp_dir, 'input.docx')
        with open(docx_path, 'wb') as temp_docx_file:
            temp_docx_file.write(docx_content.getvalue())
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', temp_dir, docx_path
        ], check=True)
        pdf_path = os.path.join(temp_dir, 'input.pdf')
        with open(pdf_path, 'rb') as temp_pdf_file:
            pdf_content = temp_pdf_file.read()
        pdf_bytes_io = BytesIO(pdf_content)
        os.remove(docx_path)
        os.remove(pdf_path)
    return pdf_bytes_io
def convert_excel_to_pdf(excel_content):
    with TemporaryDirectory() as temp_dir:
        excel_path = os.path.join(temp_dir, 'input.xlsx')
        with open(excel_path, 'wb') as temp_excel_file:
            temp_excel_file.write(excel_content.getvalue())
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', temp_dir, excel_path
        ], check=True)
        pdf_path = os.path.join(temp_dir, 'input.pdf')
        with open(pdf_path, 'rb') as temp_pdf_file:
            pdf_content = temp_pdf_file.read()
        pdf_bytes_io = BytesIO(pdf_content)
        os.remove(excel_path)
        os.remove(pdf_path)
    return pdf_bytes_io
def convert_powerpoint_to_pdf(pptx_content):
    with TemporaryDirectory() as temp_dir:
        pptx_path = os.path.join(temp_dir, 'input.pptx')
        with open(pptx_path, 'wb') as temp_pptx_file:
            temp_pptx_file.write(pptx_content.getvalue())
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', temp_dir, pptx_path], check=True)
        pdf_path = os.path.join(temp_dir, 'input.pdf')
        with open(pdf_path, 'rb') as temp_pdf_file:
            pdf_content = temp_pdf_file.read()
        pdf_bytes_io = BytesIO(pdf_content)
        os.remove(pptx_path)
        os.remove(pdf_path)
    return pdf_bytes_io

##################### File conversion Views ###################################
def text_to_pdf_view(request):
    if request.method == 'POST':
        user_file = request.FILES.get('file')
        user_filename=user_file.name
        user_file_content = BytesIO()
        for chunk in user_file.chunks():
            user_file_content.write(chunk)
        if user_file:
            pdf_content = convert_text_to_pdf(user_file)
            pdf_filename=user_file.name.replace('.txt','.pdf')
            if isActive(request):
                store_user_history(request,user_filename,user_file_content,pdf_filename,pdf_content)
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{user_file.name.replace(".txt", ".pdf")}"'
            return response
    return render(request, 'file_converter.html', {'file_accept': '.txt'})

def html_to_pdf_view(request):
    if request.method == 'POST':
        user_file = request.FILES.get('file')
        if user_file:
            user_file = request.FILES['file']
            user_filename = user_file.name
            html_file_content = BytesIO()
            for chunk in user_file.chunks():
                html_file_content.write(chunk)
            html_file_content.seek(0)
            pdf_file_content = convert_html_to_pdf(html_file_content)
            pdf_filename = os.path.splitext(user_filename)[0] + '.pdf'
            if isActive(request):
                store_user_history(request, user_filename, html_file_content, pdf_filename, pdf_file_content)
            response = HttpResponse(pdf_file_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response
    return render(request, 'file_converter.html', {'file_accept': '.html'})
def img_to_pdf_view(request):
    if request.method == 'POST':
        user_file = request.FILES.get('file')
        if user_file:
            user_filename = user_file.name
            user_file_content = BytesIO()
            for chunk in user_file.chunks():
                user_file_content.write(chunk)
            pdf_content = convert_image_to_pdf(user_file_content)
            pdf_filename = user_filename.rsplit('.', 1)[0] + '.pdf'
            if isActive(request):
                store_user_history(request, user_filename, user_file_content, pdf_filename, pdf_content)
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response
    return render(request, 'file_converter.html', {'file_accept': '.png, .jpg, .jpeg'})
def docx_to_pdf_view(request):
    if request.method == 'POST':
        user_file = request.FILES.get('file')
        if user_file:
            user_filename = user_file.name
            user_file_content = BytesIO()
            for chunk in user_file.chunks():
                 user_file_content.write(chunk)
            pdf_content = convert_docx_to_pdf(user_file_content)
            pdf_filename = user_filename.rsplit('.', 1)[0] + '.pdf'
            pdf_content_bytes = pdf_content.getvalue()
            if isActive(request):
                store_user_history(request, user_filename, user_file_content, pdf_filename, pdf_content_bytes)
            response = HttpResponse(pdf_content_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response
    return render(request, 'file_converter.html', {'file_accept': '.docx'})
def excel_to_pdf_view(request):
    if request.method == 'POST':
        user_file = request.FILES.get('file')
        if user_file:
            user_filename = user_file.name
            user_file_content = BytesIO()
            for chunk in user_file.chunks():
                user_file_content.write(chunk)
            pdf_content = convert_excel_to_pdf(user_file_content)
            pdf_filename = user_filename.rsplit('.', 1)[0] + '.pdf'
            pdf_content_bytes = pdf_content.getvalue()
            if isActive(request):
                store_user_history(request, user_filename, user_file_content, pdf_filename, pdf_content_bytes)
            response = HttpResponse(pdf_content_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response
    return render(request, 'file_converter.html', {'file_accept': '.xlsx'})
def powerpoint_to_pdf_view(request):
    if request.method == 'POST':
        user_file = request.FILES.get('file')
        if user_file:
            user_filename = user_file.name
            user_file_content = BytesIO()
            for chunk in user_file.chunks():
                user_file_content.write(chunk)
            pdf_content = convert_powerpoint_to_pdf(user_file_content)
            pdf_filename = user_filename.rsplit('.', 1)[0] + '.pdf'
            pdf_content_bytes = pdf_content.getvalue()
            if isActive(request):
                store_user_history(request, user_filename, user_file_content, pdf_filename, pdf_content_bytes)
            response = HttpResponse(pdf_content_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response
    return render(request, 'file_converter.html', {'file_accept': '.pptx'})
def texts_to_pdf_view(request):
    if request.method == 'POST':
        user_files = request.FILES.getlist('file')
        if user_files:
            pdf_contents = []
            user_filenames = [file.name for file in user_files]

            for user_file in user_files:
                user_file_content = BytesIO()
                for chunk in user_file.chunks():
                    user_file_content.write(chunk)
                pdf_content = convert_text_to_pdf(user_file_content)
                pdf_contents.append(pdf_content)

            combined_pdf_content = combine_pdfs(pdf_contents)
            pdf_filename = 'PDFMaker-generated-document.pdf'

            if isActive(request):
                store_user_history(request, ', '.join(user_filenames), None, pdf_filename, combined_pdf_content)

            response = HttpResponse(combined_pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response

    return render(request, 'file_converter.html', {'file_accept': '.txt', 'allow_multiple': True})
def htmls_to_pdf_view(request):
    if request.method == 'POST':
        user_files = request.FILES.getlist('file')
        if user_files:
            pdf_contents = []
            user_filenames = [file.name for file in user_files]

            for user_file in user_files:
                user_file_content = BytesIO()
                for chunk in user_file.chunks():
                    user_file_content.write(chunk)
                pdf_content = convert_html_to_pdf(user_file_content)
                pdf_contents.append(pdf_content)

            combined_pdf_content = combine_pdfs(pdf_contents)
            pdf_filename = 'PDFMaker-generated-document.pdf'

            if isActive(request):
                store_user_history(request, ', '.join(user_filenames), None, pdf_filename, combined_pdf_content)

            response = HttpResponse(combined_pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response

    return render(request, 'file_converter.html', {'file_accept': '.html', 'allow_multiple': True})
def imgs_to_pdf_view(request):
    if request.method == 'POST':
        user_files = request.FILES.getlist('file')
        if user_files:
            pdf_contents = []
            user_filenames = [file.name for file in user_files]

            for user_file in user_files:
                user_file_content = BytesIO()
                for chunk in user_file.chunks():
                    user_file_content.write(chunk)
                pdf_content = convert_image_to_pdf(user_file_content)
                pdf_contents.append(pdf_content)

            combined_pdf_content = combine_pdfs(pdf_contents)
            pdf_filename = 'PDFMaker-generated-document.pdf'

            if isActive(request):
                store_user_history(request, ', '.join(user_filenames), None, pdf_filename, combined_pdf_content)

            response = HttpResponse(combined_pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response

    return render(request, 'file_converter.html', {'file_accept': '.png, .jpg, .jpeg', 'allow_multiple': True})
def docxs_to_pdf_view(request):
    if request.method == 'POST':
        user_files = request.FILES.getlist('file')
        if user_files:
            pdf_contents = []
            user_filenames = [file.name for file in user_files]

            for user_file in user_files:
                user_file_content = BytesIO()
                for chunk in user_file.chunks():
                    user_file_content.write(chunk)
                pdf_content = convert_docx_to_pdf(user_file_content)
                pdf_contents.append(pdf_content)

            combined_pdf_content = combine_pdfs(pdf_contents)
            pdf_filename = 'PDFMaker-generated-document.pdf'

            if isActive(request):
                store_user_history(request, ', '.join(user_filenames), None, pdf_filename, combined_pdf_content)

            response = HttpResponse(combined_pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response

    return render(request, 'file_converter.html', {'file_accept': '.docx', 'allow_multiple': True})
def excels_to_pdf_view(request):
    if request.method == 'POST':
        user_files = request.FILES.getlist('file')
        if user_files:
            pdf_contents = []
            user_filenames = [file.name for file in user_files]

            for user_file in user_files:
                user_file_content = BytesIO()
                for chunk in user_file.chunks():
                    user_file_content.write(chunk)
                pdf_content = convert_excel_to_pdf(user_file_content)
                pdf_contents.append(pdf_content)

            combined_pdf_content = combine_pdfs(pdf_contents)
            pdf_filename = 'PDFMaker-generated-document.pdf'

            if isActive(request):
                store_user_history(request, ', '.join(user_filenames), None, pdf_filename, combined_pdf_content)

            response = HttpResponse(combined_pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response

    return render(request, 'file_converter.html', {'file_accept': '.xlsx', 'allow_multiple': True})
def powerpoints_to_pdf_view(request):
    if request.method == 'POST':
        user_files = request.FILES.getlist('file')
        if user_files:
            pdf_contents = []
            user_filenames = [file.name for file in user_files]

            for user_file in user_files:
                user_file_content = BytesIO()
                for chunk in user_file.chunks():
                    user_file_content.write(chunk)
                pdf_content = convert_powerpoint_to_pdf(user_file_content)
                pdf_contents.append(pdf_content)

            combined_pdf_content = combine_pdfs(pdf_contents)
            pdf_filename = 'PDFMaker-generated-document.pdf'

            if isActive(request):
                store_user_history(request, ', '.join(user_filenames), None, pdf_filename, combined_pdf_content)

            response = HttpResponse(combined_pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response

    return render(request, 'file_converter.html', {'file_accept': '.pptx', 'allow_multiple': True})

def multi_formats_to_pdf_view(request):
    if request.method == 'POST':
        user_files = request.FILES.getlist('file')
        if user_files:
            pdf_contents = []
            user_filenames = [file.name for file in user_files]

            for user_file in user_files:
                user_file_content = BytesIO()
                for chunk in user_file.chunks():
                    user_file_content.write(chunk)

                file_extension = user_file.name.lower().split('.')[-1]

                if file_extension == 'txt':
                    pdf_content = convert_text_to_pdf(user_file_content)
                elif file_extension == 'html':
                    pdf_content = convert_html_to_pdf(user_file_content)
                elif file_extension in ['jpg', 'jpeg', 'png']:
                    pdf_content = convert_image_to_pdf(user_file_content)
                elif file_extension == 'docx':
                    pdf_content = convert_docx_to_pdf(user_file_content)
                elif file_extension == 'xlsx':
                    pdf_content = convert_excel_to_pdf(user_file_content)
                elif file_extension == 'pptx':
                    pdf_content = convert_powerpoint_to_pdf(user_file_content)
                else:
                    continue  # Skip unsupported file types


                pdf_contents.append(pdf_content)

            combined_pdf_content = combine_pdfs(pdf_contents)
            pdf_filename = 'PDFMaker-generated-document.pdf'

            if isActive(request):
                store_user_history(request, ', '.join(user_filenames), None, pdf_filename, combined_pdf_content)

            response = HttpResponse(combined_pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response

    return render(request, 'file_converter.html', {'file_accept': '.docx, .txt, .jpg, .jpeg, .png, .pptx, .xlsx', 'allow_multiple': True})

#----------------------------Feedback------------------------------------------#

def feedback_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        APP = 'PDF_Maker'
        admin_gmail = 'feedback.s5tech@gmail.com'
        feedback_type = request.POST.get('feedback')
        message = request.POST.get('message')
        email_subject = f'{APP}-feedback'
        from_email = 's5tech.sendmail@gmail.com'
        to_email = [admin_gmail]
        text_content = f'Name: {name}\n\nEmail: {email}\n\nFeedback Type: {feedback_type}\n\nMessage: {message}'
        email_message = EmailMultiAlternatives(
            email_subject,
            text_content,
            from_email,
            to_email,
        )
        files = request.FILES.getlist('files')
        for f in files:
            email_message.attach(f.name, f.read(), f.content_type)
        email_message.send(fail_silently=False)
        return redirect('home')
    return render(request, 'feedback.html')
def privacy_policy_view(request):
    return render(request,'privacy_policy.html')
def terms_and_conditions_view(request):
    return render(request,'terms_and_conditions.html')