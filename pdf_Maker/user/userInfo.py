from user.models import UserInformation

def userInformation(request):
    user_id = request.session.get('user_id',None)
    user_information = None
    
    try:
        if user_id is not None:
            user_information = UserInformation.objects.get(pk=user_id)
        else:
        #     # emergency fix default object
            user_information = UserInformation.objects.get(pk=1)
            

    except Exception as e:
        print(f'An error occurred: {e}')
       


    data = {'user': user_information}
    return data
