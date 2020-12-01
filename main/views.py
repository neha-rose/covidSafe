# Create your views here.

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from forms import RegisterForm

def welcomepage(request):
    return render(request, "main/welcome.html", {})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})