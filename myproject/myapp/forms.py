from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import USER_TYPE_CHOICES, MyUser

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2', 'usertype']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usertype'].widget = forms.Select(choices=USER_TYPE_CHOICES)
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.usertype = self.cleaned_data['usertype']  
        if commit:
            user.save()
        return user
    
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        max_length=50,
        min_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        error_messages={
            'required': 'Please enter your username.',
            'min_length': 'Username must be at least 5 characters long.',
            'max_length': 'Username cannot exceed 50 characters.'
        }
    )
    password = forms.CharField(
        label="Password",
        min_length=6,
        max_length=80,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        error_messages={
            'required': 'Please enter your password.',
            'min_length': 'Password must be at least 6 characters long.',
            'max_length': 'Password cannot exceed 80 characters.'
        }
    )
    remember = forms.BooleanField(
        label="Remember Me",
        required=False
    )
