from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from .forms import SCMUserForm,UserForm

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('postlogin') 
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
    return render(request, 'user/dashboard.html')

def  signup_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('postlogin') 
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
                user.save()
                scm_user.user = user
                scm_user.save()
                customer_group = Group.objects.get_or_create(name='SCM_USER')
                customer_group[0].user_set.add(user)
                messages.success(request, "User account successfully!")
                return HttpResponseRedirect('/user/login')
            else:
                messages.error(request, user_form.errors)
                messages.error(request, scmuser_form.errors)
        except Exception as e:
            print('signup exception: ',e)
            messages.error(request, 'unable to register')
    data['userForm'] = user_form
    data['scmuserForm'] = scmuser_form
    return render(request, 'home/signup.html', context= data)
