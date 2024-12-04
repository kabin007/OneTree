from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Food,Address

class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username', 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email', 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter your password', 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password', 'class': 'form-control'})


class LoginForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password']


class FoodForm(forms.ModelForm):
    class Meta:
        model=Food
        fields=['name','description','price','rating','category_name','delivery_time','food_image']



class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['fullname','address','ward','area','mobile']