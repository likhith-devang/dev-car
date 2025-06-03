from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'car_type', 'daily_rate', 'description', 'image', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'daily_rate': forms.NumberInput(attrs={'min': 0}),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2'] 