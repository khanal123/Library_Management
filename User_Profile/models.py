from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        # hashed = make_password(password)
        # user.set_password(hashed)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class MyUser(AbstractBaseUser,PermissionsMixin):
    # username = models.CharField(max_length=150, unique=True)
    # username = None
    name = models.CharField(max_length = 20 )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

        

    


# class UserProfile(models.Model):
#     user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True)
#     location = models.CharField(max_length=50, blank=True)

#     def __str__(self):
#         return self.user.username
