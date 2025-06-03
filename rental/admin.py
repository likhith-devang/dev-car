from django.contrib import admin
from .models import Car, Driver, Rental

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'get_car_type_display', 'get_daily_rate_display', 'available')
    list_filter = ('car_type', 'available', 'year')
    search_fields = ('make', 'model', 'description')
    
    def get_daily_rate_display(self, obj):
        return obj.get_daily_rate_display()
    get_daily_rate_display.short_description = 'Daily Rate'

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'phone_number')
    search_fields = ('user__username', 'license_number', 'phone_number')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('car', 'customer', 'driver', 'start_date', 'end_date', 'status', 'total_cost')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('car__make', 'car__model', 'customer__username')
