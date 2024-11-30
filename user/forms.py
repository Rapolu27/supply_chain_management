from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models
class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name','username','email']

class SCMUserForm(forms.ModelForm):
    class Meta:
        model=models.SCMUser
        fields=['address','mobile']
