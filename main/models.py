from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cust_id = models.AutoField(primary_key=True)
    cust_name = models.CharField(max_length=200)
    cust_age = models.IntegerField()
    cust_ph_no = models.BigIntegerField()
    cust_address = models.TextField()

    def __str__(self):
        return self.cust_name

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=200)
    emp_age = models.IntegerField()
    emp_ph_no = models.BigIntegerField()
    emp_address = models.TextField()

    def __str__(self):
        return self.emp_name

class StoreVisit(models.Model):
    visit_id = models.AutoField(primary_key=True)
    body_temp = models.DecimalField(max_digits=5,decimal_places=2)
    visit_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    cust_id = models.ForeignKey(Customer,on_delete=models.CASCADE)

class HomeDeliveryOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField()
    order_time = models.TimeField()
    cust_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    emp_id = models.ForeignKey(Employee,on_delete=models.CASCADE)
  
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username