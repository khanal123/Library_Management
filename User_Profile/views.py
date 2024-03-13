from django.db.models import Q
from django.conf import settings

from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models import MyUser

# from .serializers import ProfileSerializer , UserSerializer, LoginSerializer , SignupSerializer, MyTokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .utils import accessfunction
from rest_framework import viewsets, status
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, api_view

# @api_view(['GET'])
# def api_root(request, format = None):
#         return Response(
#              {
#                 'users' : reverse('user-list', request= request , format= format ),
#                 'login' : reverse('login-list', request= request , format = format),
#              }
#         )


class UserRegisteredView(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class LoginViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    # def create(self, request, *args, **kwargs):
    #     # Dummy create method to satisfy the requirements
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # @action(detail= False, methods=['create'])
    def create(self, request, *args, **kwargs):
        response = Response()
        data = {
            "email": request.data.get("email"),
            "password": request.data.get("password"),
        }

        serializer = LoginSerializer(data=data)

        if serializer.is_valid():
            print(request.data)
            print(serializer.validated_data)
            user = serializer.validated_data
            # print(list(user.values())[0])
            # refresh = RefreshToken.for_user( list(user.values())[0])
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            response.set_cookie("refresh", refresh, httponly=True)
            response.set_cookie("access", access, httponly=True)

            return response

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# class UserProfileListCreateView(generics.ListCreateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = ProfileSerializer

# class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = ProfileSerializer

# class SignUpView(generics.CreateAPIView):
#     queryset = MyUser.objects.all()
#     serializer_class = SignupSerializer
#     permission_classes = [permissions.AllowAny]

#     def perform_create(self, serializer):
#         user = serializer.save()
#         UserProfile.objects.create(user=user)

# class LoginView(generics.CreateAPIView):
#     queryset = MyUser.objects.all()
#     serializer_class = LoginSerializer
#     permission_classes = [permissions.AllowAny]

#     def post(self, request, *args, **kwargs):
#         response = Response()
#         serializer = self.get_serializer(data=request.data)
#         # serializer = LoginSerializer(data=request.data, context={'request':request})
#         if serializer.is_valid(raise_exception=True):
#             id= serializer.validated_data['id']
#             # password = serializer.data['password']
#             print(id)

#             # Find user by username or id
#             # user = MyUser.objects.filter(Q(username=username_or_id) | Q(id=username_or_id)).first()

#             refresh = RefreshToken.for_user(id)
#             access = refresh.access_token

#             # refresh = data['refresh']

#              # Create a Response object
#             response = Response({'message': 'Login successful'})

#             # Set the cookie
#             response.set_cookie('refresh', refresh,httponly= True)
#             response.set_cookie('access',access,httponly=True)

#             return response

#         return Response({'error': 'Invalid credentials'}, status=400)

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
