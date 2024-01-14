from userData.models import userdata

def userInfo(request):
    user_id = request.session.get('user_id')
    user_information=None
    data={'user':user_information
    }
    
    try:
        user_information=userdata.objects.get(pk=user_id)
       
    except Exception:
        pass
    return data