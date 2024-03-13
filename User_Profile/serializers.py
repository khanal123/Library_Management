from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth.models import User
from .models import  MyUser
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields =['email','name','password']

    def create(self, validated_data):
        user = MyUser.objects.create(email = validated_data['email'],name = validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    def validate(self, attrs):
        data = super().validate(attrs) 
        return data
# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = UserProfile
#         fields = '__all__'

# class SignupSerializer(serializers.ModelSerializer):
#     email = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = MyUser
#         fields = ['username','email','password']
#     def create(self, validated_data):
#         validated_data["password"] = make_password(validated_data.get("password"))
#         user = MyUser.objects.create(**validated_data)
#         return user
#         # return super((SignupSerializer,self).create(validated_data))

# class LoginSerializer(serializers.Serializer):    
#     email = serializers.CharField()
# password = serializers.CharField(write_only=True)
#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')
#         # if email and password:
#         # user =  MyUser.objects.get(email = email ,password = password)
#         # print(f'from serializer = {user.id}')

#         try:
#             # user = MyUser.objects.get(email=email, password=password)
#             user = authenticate(email=email, password= password)
#                                 # ,password = password)
#             print(f'from serializer = {user}')
#         except MyUser.DoesNotExist:
#             raise serializers.ValidationError("Invalid credentials. Please try again.")
#         return {
#                 'id':user
#         }
        




        # # Add custom claims
        # token['user_id'] = user.pk
        # token['username'] = user.username

        # return token
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)
    def validate(self, data):
        print(data)
        email = data.get('email')
        password = data.get('password')
        if email and password:
            try:
                user= MyUser.objects.get(email = email)
                if user.check_password(password):                  
                    return  user
                else:
                    raise serializers.ValidationError("Incorrect Password")
            except MyUser.DoesNotExist:
                raise serializers.ValidationError("User not found")
        raise serializers.ValidationError("Both email and password are required")
    
    # def create(self, validated_data):
    #     pass  
            
            
            
        

