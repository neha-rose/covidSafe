from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    shop_name = forms.CharField(max_length=30, required=True, help_text='Enter name of the shop')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')
    admin_password = forms.CharField(widget= forms.PasswordInput)
 
    class Meta:
        model = User
        fields = ( 'username', 'shop_name', 'email', 'password1', 'password2', 'admin_password')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.shop_name = self.cleaned_data['shop_name']
        user.admin_password = self.cleaned_data['admin_password']
        if commit:
            user.save()
        return user