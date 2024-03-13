from django.shortcuts import redirect
from functools import wraps
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response

def loginrequired(function = None , session_key ='user'):
    def decorator(view_func):
        @wraps(view_func)
        def f(self, request, *args ,**kwargs):
            try:
                print("Hello")
                token = request.COOKIES.get('access')
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                return view_func(self, request,user_id,*args,**kwargs)
            except Exception as e:
                print(f"Error decoding token:{e}")
                return Response  (f"Error decoding token:{e}")              
        return f
          
    # if function is not None:
    #     return decorator(function)
    return decorator
        #No to no 13