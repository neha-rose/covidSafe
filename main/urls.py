"""covidSafe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


app_name = "main"

urlpatterns = [
    path('',views.welcomepage , name='welcomepage'),
    path("register/", views.register, name="register"),
    path("login/", views.login_req, name="login"),
    path("logout", views.logout_req, name="logout"),
    path("home/", views.homepage, name="home"),
    path("store-visit/", views.storevisit, name="storevisit"),
    path("home-delivery/", views.homedelivery, name="homedelivery"),
    path("contact-tracing-storevisit/", views.contacttracing_sv, name="contacttracing_sv"),
    path("contact-tracing-homedelivery/", views.contacttracing_hd, name="contacttracing_hd"),
    path("add-employee/", views.addemployee, name="addemployee"),
    path("edit-employee/", views.editemployee, name="editemployee"),
    path("select-employee/", views.selectemployee, name="selectemployee"),
    path("settings/", views.settings, name="settings"),
    path("change-password/", views.changepassword, name="changepassword"),
    path("add-customer/", views.addcustomer, name="addcustomer"),
    path("edit-customer/", views.editcustomer, name="editcustomer"),
]
