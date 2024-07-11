from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Food




class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class LoginForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password']


class FoodForm(forms.ModelForm):
    class Meta:
        model=Food
        fields=['name','description','price','rating','category_name','delivery_time','food_image']
