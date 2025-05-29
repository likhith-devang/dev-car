from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'car_type', 'daily_rate', 'description', 'image', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'daily_rate': forms.NumberInput(attrs={'min': 0}),
        } 