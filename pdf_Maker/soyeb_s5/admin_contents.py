from soyeb_s5.models import Follow_Me,ContactInformation

def follow_me(request):
    followMe = Follow_Me.objects.all()
    return {'followMe': followMe}

def contact_me(request):
    contactMe = ContactInformation.objects.all()
    return {'contactMe':contactMe}
