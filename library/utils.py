from rest_framework_simplejwt.tokens import AccessToken
def accessfunction(request):
    try:
        print("Hello")
        token = request.COOKIES.get('access')
        if not token:
            return None
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        return user_id
    except KeyError:
        return None
    except Exception as e:
        print(f"Error decoding token:{e}")
        return None
    