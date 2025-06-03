from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Car, Driver, Rental
from django.db.models import Q
from datetime import datetime
from .forms import CarForm, UserRegistrationForm
from django.contrib.auth import login

def home(request):
    cars = Car.objects.filter(available=True)
    return render(request, 'rental/home.html', {'cars': cars})

def car_list(request):
    car_type = request.GET.get('type')
    search_query = request.GET.get('search')
    
    cars = Car.objects.filter(available=True)
    
    if car_type:
        cars = cars.filter(car_type=car_type)
    
    if search_query:
        cars = cars.filter(
            Q(make__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    return render(request, 'rental/car_list.html', {
        'cars': cars,
        'car_types': Car.CAR_TYPES
    })

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'rental/car_detail.html', {'car': car})

@login_required
def create_rental(request, car_id):
    if request.method == 'POST':
        car = get_object_or_404(Car, id=car_id)
        
        # Get form data
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        pickup_time = request.POST.get('pickup_time')
        need_driver = request.POST.get('need_driver') == 'on'
        pickup_location = request.POST.get('pickup_location')
        
        # Convert dates to datetime objects
        start_datetime = datetime.strptime(f"{start_date} {pickup_time}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{end_date} {pickup_time}", "%Y-%m-%d %H:%M")
        
        # Make them timezone-aware
        start_datetime = timezone.make_aware(start_datetime)
        end_datetime = timezone.make_aware(end_datetime)
        
        # Validate dates
        if start_datetime < timezone.now():
            messages.error(request, "Start date cannot be in the past")
            return redirect('car_detail', car_id=car_id)
        
        if end_datetime <= start_datetime:
            messages.error(request, "End date must be after start date")
            return redirect('car_detail', car_id=car_id)
        
        # Check if car is available for the selected dates
        if not car.is_available(start_datetime, end_datetime):
            messages.error(request, "Car is not available for the selected dates")
            return redirect('car_detail', car_id=car_id)
        
        # Calculate total cost
        days = (end_datetime - start_datetime).days
        total_cost = car.daily_rate * days
        
        # Create rental
        rental = Rental.objects.create(
            car=car,
            customer=request.user,
            start_date=start_datetime,
            end_date=end_datetime,
            pickup_location=pickup_location if need_driver else None,
            pickup_time=pickup_time if need_driver else None,
            total_cost=total_cost,
            status='pending'
        )
        
        # Mark car as unavailable
        car.available = False
        car.save()
        
        # Assign driver if needed
        if need_driver:
            if not pickup_location:
                messages.error(request, "Pickup location is required when requesting a driver")
                rental.delete()
                return redirect('car_detail', car_id=car_id)
                
            available_driver = Driver.objects.filter(is_available=True).first()
            if available_driver:
                rental.driver = available_driver
                rental.save()
                messages.success(request, "Driver assigned successfully")
            else:
                messages.warning(request, "No drivers available at the moment")
        
        messages.success(request, "Car rented successfully!")
        return redirect('user_dashboard')
    
    return redirect('car_detail', car_id=car_id)

@login_required
def user_dashboard(request):
    user_rentals = Rental.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'rental/dashboard.html', {'rentals': user_rentals})

@login_required
def cancel_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, customer=request.user)
    
    if rental.status == 'pending':
        rental.status = 'cancelled'
        rental.save()
        messages.success(request, 'Rental cancelled successfully')
    else:
        messages.error(request, 'Cannot cancel this rental')
    
    return redirect('user_dashboard')

@login_required
def car_edit(request, car_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit cars.')
        return redirect('car_detail', car_id=car_id)
        
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car details updated successfully!')
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)
    return render(request, 'rental/car_edit.html', {'form': form, 'car': car})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Car Rental.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'rental/register.html', {'form': form})
