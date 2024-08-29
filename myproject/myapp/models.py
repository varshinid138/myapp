from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

USER_TYPE_CHOICES = [
    ('superuser', 'Superuser'),
    ('admin', 'Admin'),
    ('user', 'User'),
]

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        
        if 'usertype' not in extra_fields:
            raise ValueError('The usertype field must be set')
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    usertype = models.CharField(max_length=50,choices=USER_TYPE_CHOICES)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','usertype']

    def get_user(self):
        return self.username
