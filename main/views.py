# Create your views here.

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Customer


def welcomepage(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        return render(request, "main/welcome.html", {})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect('main:home')
        else:
            messages.error(request, f"Your password can't be too similar to your other personal information or a commonly used password.")
            messages.error(request, f"Your password must contain atleast 8 characters and can't be entirely numeric.")
    else:
        form = RegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'main/register.html', {'form': form, 'profile_form': profile_form})

def login_req(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('main:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = 'main/login.html',
                    context={"form":form})

def logout_req(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:welcomepage")  

def homepage(request):
    context = {'customers': Customer.objects.all}
    return render(request, "main/home.html", context)  

def storevisit(request):
    return render(request, "main/storevisit.html", {})

def homedelivery(request):
    return render(request, "main/homedelivery.html", {})

            
