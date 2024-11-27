from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SCMUser,UserForm

def login_view(request):
    form = UserForm()
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
            form.add_error(None, 'Invalid username or password')
    return render(request, 'home/login.html',context = {'form': form})

def dashboard_view(request):
    return render(request, 'user/dashboard.html')

