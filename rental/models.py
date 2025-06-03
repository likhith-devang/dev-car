from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

class Car(models.Model):
    CAR_TYPES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('sports', 'Sports Car'),
        ('luxury', 'Luxury Car'),
        ('passenger', 'Passenger Vehicle'),
        ('goods', 'Goods Vehicle'),
    ]
    
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    car_type = models.CharField(max_length=20, choices=CAR_TYPES)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)  # Now in rupees
    description = models.TextField()
    image = models.ImageField(upload_to='cars/', null=True, blank=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"
    
    def get_daily_rate_display(self):
        return f"₹{self.daily_rate:,.2f}"
    
    def is_available(self, start_date, end_date):
        if not self.available:
            return False
            
        # Check if there are any overlapping rentals
        overlapping_rentals = Rental.objects.filter(
            car=self,
            status__in=['pending', 'active'],
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        return not overlapping_rentals.exists()

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.license_number}"

class Rental(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    pickup_location = models.TextField(null=True, blank=True)
    pickup_time = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Rental #{self.id} - {self.car} - {self.customer}"
