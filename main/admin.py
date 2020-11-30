from django.contrib import admin
from .models import Customer, Employee, StoreVisit, HomeDeliveryOrder

# Register your models here.
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(StoreVisit)
admin.site.register(HomeDeliveryOrder)