from userData.models import userdata

def userInformation(request):
    user_id = request.session.get('user_id',None)
    print(user_id)
    user_information = None
    
    try:
        if user_id is not None:
            user_information = userdata.objects.get(pk=user_id)
        else:
            # emergency fix default object
            user_information = userdata.objects.get(pk=1)
            
            
    except userdata.DoesNotExist:
        print('User not found')
    except Exception as e:
        print(f'An error occurred: {e}')

    data = {'user': user_information}
    return data
