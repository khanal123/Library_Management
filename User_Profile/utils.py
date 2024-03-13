from rest_framework_simplejwt.tokens import AccessToken
def accessfunction(request):
    token = request.COOKIES.get('access')
    access_token = AccessToken(token)
    print(AccessToken)