from userData.models import userdata

def userInformation(request):
    user_id = request.session.get('user_id')
    user_information=None
    
    
    try:
        user_information=userdata.objects.get(pk=user_id)
        
       
    except Exception:
        print('excep')
    data={'user':user_information
    }
    return data