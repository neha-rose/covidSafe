from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile, StoreVisit, HomeDeliveryOrder, Employee, Customer


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
        fields = ('shop_name',)

class StoreVisitForm(forms.ModelForm):
    class Meta:
        model = StoreVisit
        fields = ( 'visit_date', 'body_temp', 'check_in_time', 'check_out_time')

class HomeDeliveryOrderForm(forms.ModelForm):
    class Meta:
        model = HomeDeliveryOrder
        fields = ( 'order_date', 'emp_id', 'order_time')

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ( 'cust_name', 'cust_age', 'cust_ph_no', 'cust_address') 
        widgets = {
            'cust_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cust_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'cust_ph_no': forms.TextInput(attrs={'class': 'form-control'}),
            'cust_address': forms.TextInput(attrs={'class': 'form-control'}),
        }  
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ( 'emp_name', 'emp_age', 'emp_ph_no', 'emp_address')
        widgets = {
            'emp_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'emp_ph_no': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_address': forms.TextInput(attrs={'class': 'form-control'}),
        }
