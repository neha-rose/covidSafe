from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    shop_name = forms.CharField(max_length=30, required=True, help_text='Enter name of the shop')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')
    adminpw = forms.CharField(widget= forms.PasswordInput)
    }    
    class Meta:
        model = User
        fields = ( 'shop_name', 'email', 'password1', 'password2', 'adminpw')