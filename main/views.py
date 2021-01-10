# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, UserProfileForm, StoreVisitForm, HomeDeliveryOrderForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Customer, Employee, StoreVisit, HomeDeliveryOrder
from django.core.paginator import Paginator
import datetime
from dateutil.relativedelta import relativedelta

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
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{error}")
            for error in form.non_field_errors():
                messages.error(request, f"{error}")
            for field in profile_form:
                for error in field.errors:
                    messages.error(request, f"{error}")
            for error in profile_form.non_field_errors():
                messages.error(request, f"{error}")
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

@login_required
def homepage(request):
    customers = Customer.objects.filter(user=request.user)
    searched_customer = request.GET.get('searched_customer')
    if searched_customer:
        search_list = customers.filter(cust_name__icontains=searched_customer)
        p = Paginator(search_list, 10)
        page_num = request.GET.get('page', 1)
        page = p.page(page_num)
    else:
        page = None
        search_list = None
    customer_id = request.POST.get('cust')
    func = request.POST.get('func')
    if func=='edit':
        if customer_id is None:
            messages.warning(request, f"No customer selected!")
        else:
            return redirect(reverse('main:editcustomer')+'?cust=%s' %customer_id)
    elif func=='storevisit':
        if customer_id is None:
            messages.warning(request, f"No customer selected!")
        else:
            return redirect(reverse('main:storevisit')+'?cust=%s' %customer_id)
    elif func=='homedelivery':
        if customer_id is None:
            messages.warning(request, f"No customer selected!")
        else:
            return redirect(reverse('main:homedelivery')+'?cust=%s' %customer_id)
    elif func=='contacttracing':
        if customer_id is None:
            messages.warning(request, f"No customer selected!")
        else:
            return redirect(reverse('main:contacttracing_sv')+'?cust=%s' %customer_id)
    context = {'page': page, 'searched_customer': searched_customer, 'search_list': search_list}
    return render(request, "main/home.html", context)

@login_required
def storevisit(request):
    customer_id = request.GET.get('cust')
    if customer_id is None:
        messages.warning(request, f"No customer selected!")
        return redirect('main:home')
    customers = Customer.objects.filter(user=request.user)
    try:
        cust = customers.get(cust_id=customer_id)
    except:
        messages.error(request, f"Customer doesn't exist!")
        return redirect('main:home')
    if request.method == 'POST':
        form = StoreVisitForm(request.POST)
        if form.is_valid():
            storevisit = form.save(commit=False)
            storevisit.cust_id = cust
            storevisit.save()
            messages.success(request, f"Store visit information recorded!")
            return redirect('main:home')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{error}")
            for error in form.non_field_errors():
                messages.error(request, f"{error}")
    else:
        form = StoreVisitForm()
    return render(request, "main/storevisit.html", {'form': form})      
    
@login_required
def homedelivery(request):
    employees = Employee.objects.filter(user=request.user)
    customer_id = request.GET.get('cust')
    if customer_id is None:
        messages.warning(request, f"No customer selected!")
        return redirect('main:home')
    customers = Customer.objects.filter(user=request.user)
    try:
        cust = customers.get(cust_id=customer_id)
    except:
        messages.error(request, f"Customer doesn't exist!")
        return redirect('main:home')
    if request.method == 'POST':
        form = HomeDeliveryOrderForm(request.POST)
        if form.is_valid():
            homedelivery = form.save(commit=False)
            homedelivery.cust_id = cust
            homedelivery.save()
            messages.success(request, f"Home delivery information recorded!")
            return redirect('main:home')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{error}")
            for error in form.non_field_errors():
                messages.error(request, f"{error}")
    else:
        form = HomeDeliveryOrderForm()
    return render(request, "main/homedelivery.html", {'form': form, 'employees': employees})      
    
@login_required
def contacttracing_sv(request):
    customer_id = request.GET.get('cust')
    if customer_id is None:
        messages.warning(request, f"No customer selected!")
        return redirect('main:home')
    customers = Customer.objects.filter(user=request.user)
    try:
        cust = customers.get(cust_id=customer_id)
    except:
        messages.error(request, f"Customer doesn't exist!")
        return redirect('main:home')
    storevisits = cust.storevisit_set.all().order_by('-visit_date','-check_in_time')
    contacts = []
    other_storevisits = StoreVisit.objects.all().exclude(cust_id=cust)
    for storevisit in storevisits:
        for other_storevisit in other_storevisits:
            if other_storevisit.visit_date == storevisit.visit_date:
                if (other_storevisit.check_in_time >= storevisit.check_in_time and other_storevisit.check_in_time <= storevisit.check_out_time) or (other_storevisit.check_out_time >= storevisit.check_in_time and other_storevisit.check_out_time <= storevisit.check_out_time) or (other_storevisit.check_in_time <= storevisit.check_in_time and other_storevisit.check_out_time >= storevisit.check_out_time):
                    contacts.append(other_storevisit)
    p = Paginator(contacts, 20)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    now = datetime.datetime.now()
    two_months_before = now + relativedelta(months=-2)
    context = {'page': page, 'cust': cust, 'two_months_before': two_months_before, 'storevisits': storevisits}
    return render(request, "main/contacttracing_sv.html", context)

@login_required
def contacttracing_hd(request):
    customer_id = request.GET.get('cust')
    if customer_id is None:
        messages.warning(request, f"No customer selected!")
        return redirect('main:home')
    customers = Customer.objects.filter(user=request.user)
    try:
        cust = customers.get(cust_id=customer_id)
    except:
        messages.error(request, f"Customer doesn't exist!")
        return redirect('main:home')
    homedeliveryorders = cust.homedeliveryorder_set.all().order_by('-order_date','-order_time')
    p = Paginator(homedeliveryorders, 20)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    return render(request, "main/contacttracing_hd.html", {'page': page, 'cust': cust})