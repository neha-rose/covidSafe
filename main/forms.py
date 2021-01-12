from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, StoreVisit, HomeDeliveryOrder, Customer

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')
 
    class Meta:
        model = User
        fields = ( 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'shop_name', 'admin_password')
        widgets = {
            'password': forms.PasswordInput()
        }

class StoreVisitForm(forms.ModelForm):
    class Meta:
        model = StoreVisit
        fields = ( 'visit_date', 'body_temp', 'check_in_time', 'check_out_time')

class HomeDeliveryOrderForm(forms.ModelForm):
    class Meta:
        model = HomeDeliveryOrder
        fields = ( 'order_date', 'emp_id', 'order_time')

class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ( 'cust_id', 'cust_name', 'cust_age', 'cust_ph_no', 'cust_address')        
