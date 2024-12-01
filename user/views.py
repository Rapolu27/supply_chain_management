from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from scm_core.exception import UserException
from scm_core import validator
from scm_core.inventory_threshold import get_out_of_range_products
from .forms import SCMUserForm,UserForm
from scm.models import Product, Supplier,Inventory, PurchaseOrder
from datetime import date
def login_view(request):
    if request.user.is_authenticated:
        return redirect('postlogin') 
    form = UserForm()
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password1')
            print('username: ', username, 'password: ',password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login success")
                return redirect('/postlogin')  # Redirect to home page after successful login
            else:
                messages.error(request, 'Invalid username or password.')
    except Exception as e:
        print('login error: ',str(e))
        messages.error(request, 'Invalid username or password');
    return render(request, 'home/login.html',context = {'form': form})

@login_required(login_url='user_login')
def dashboard_view(request):
    data = {}
    try:
        total_products = Product.objects.all().count()
        active_orders = PurchaseOrder.objects.filter(status='Pending').count()
        active_suppliers = Supplier.objects.all().count() 
        data['metrics'] = {'total_products':total_products, 'active_orders':active_orders, 'active_suppliers':active_suppliers}
        today_deliveries = PurchaseOrder.objects.filter(delivery_date=date.today())
        data['today_deliveries'] = today_deliveries
        print('total_deliveries', today_deliveries)
        out_of_range_products = get_out_of_range_products(Inventory.objects.all())
        data['out_of_range'] = out_of_range_products
    except Exception as e:
        print("dashboard exception", e)
        messages.error(request, "Unable to load metrics")
    return render(request, 'user/dashboard.html', context=data)

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('postlogin') 
    data = {}
    user_form = UserForm()
    scmuser_form = SCMUserForm() 
    if request.method == 'POST':
        try:
            user_form= UserForm(request.POST)
            scmuser_form = SCMUserForm(request.POST)
            if user_form.is_valid() and scmuser_form.is_valid():
                user = user_form.save(commit=False)
                scm_user =  scmuser_form.save(commit=False)
                validator.validate_username(user.username)
                validator.validate_mobile_number(scm_user.mobile)
                validator.validate_address_length(scm_user.address)
                user.save()
                scm_user.user = user
                scm_user.save()
                scm_user_group = Group.objects.get_or_create(name='SCM_USER')
                scm_user_group[0].user_set.add(user)
                messages.success(request, "Registration successfully!")
                return HttpResponseRedirect('/user/login')
            else:
                messages.error(request, user_form.errors)
                messages.error(request, scmuser_form.errors)
        except UserException as e:
            messages.error(request, str(e))
        except Exception as e:
            print('signup exception: ',e)
            messages.error(request, 'unable to register')
    data['userForm'] = user_form
    data['scmuserForm'] = scmuser_form
    return render(request, 'home/signup.html', context= data)
