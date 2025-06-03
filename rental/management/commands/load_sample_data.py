from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rental.models import Car, Driver
import os
from django.core.files import File
from django.conf import settings
import requests
from tempfile import NamedTemporaryFile

class Command(BaseCommand):
    help = 'Loads sample data for the car rental application'

    def handle(self, *args, **kwargs):
        # Sample car data with image URLs
        cars_data = [
            # Budget Sedans
            {
                'make': 'Suzuki',
                'model': 'Swift',
                'year': 2023,
                'car_type': 'sedan',
                'daily_rate': 30,
                'description': 'Fuel-efficient compact sedan perfect for city driving and daily commutes.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1617469767053-3c4f2a69cffd?w=800'
            },
            {
                'make': 'Hyundai',
                'model': 'i20',
                'year': 2023,
                'car_type': 'sedan',
                'daily_rate': 35,
                'description': 'Stylish and economical hatchback with modern features and great fuel efficiency.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1617469767053-3c4f2a69cffd?w=800'
            },
            {
                'make': 'Maruti',
                'model': 'Ciaz',
                'year': 2023,
                'car_type': 'sedan',
                'daily_rate': 40,
                'description': 'Comfortable mid-size sedan with excellent fuel economy and spacious interior.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1617469767053-3c4f2a69cffd?w=800'
            },
            # Budget SUVs
            {
                'make': 'Mahindra',
                'model': 'XUV300',
                'year': 2023,
                'car_type': 'suv',
                'daily_rate': 45,
                'description': 'Compact SUV with rugged design and good ground clearance for city and highway driving.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800'
            },
            {
                'make': 'Tata',
                'model': 'Nexon',
                'year': 2023,
                'car_type': 'suv',
                'daily_rate': 42,
                'description': 'Modern compact SUV with advanced safety features and comfortable ride.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800'
            },
            {
                'make': 'Kia',
                'model': 'Sonet',
                'year': 2023,
                'car_type': 'suv',
                'daily_rate': 48,
                'description': 'Feature-rich compact SUV with premium interior and excellent value for money.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800'
            },
            # Existing cars
            {
                'make': 'Toyota',
                'model': 'Camry',
                'year': 2023,
                'car_type': 'sedan',
                'daily_rate': 50,
                'description': 'Comfortable and reliable sedan perfect for family trips.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1617469767053-3c4f2a69cffd?w=800'
            },
            {
                'make': 'Honda',
                'model': 'CR-V',
                'year': 2023,
                'car_type': 'suv',
                'daily_rate': 65,
                'description': 'Spacious SUV with excellent fuel efficiency and modern features.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800'
            },
            {
                'make': 'BMW',
                'model': 'M3',
                'year': 2023,
                'car_type': 'sports',
                'daily_rate': 120,
                'description': 'High-performance luxury sports car with cutting-edge technology.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1607853202273-797f1c22a38e?w=800'
            },
            {
                'make': 'Mercedes-Benz',
                'model': 'S-Class',
                'year': 2023,
                'car_type': 'luxury',
                'daily_rate': 150,
                'description': 'Ultimate luxury sedan with premium features and comfort.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800'
            },
            {
                'make': 'Tesla',
                'model': 'Model 3',
                'year': 2023,
                'car_type': 'electric',
                'daily_rate': 90,
                'description': 'Electric sedan with impressive range and autopilot features.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1617704548623-340376564e68?w=800'
            },
            {
                'make': 'Ford',
                'model': 'Mustang',
                'year': 2023,
                'car_type': 'sports',
                'daily_rate': 100,
                'description': 'Iconic American muscle car with powerful performance.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?w=800'
            },
            {
                'make': 'Audi',
                'model': 'Q5',
                'year': 2023,
                'car_type': 'suv',
                'daily_rate': 85,
                'description': 'Luxury SUV with quattro all-wheel drive and premium interior.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800'
            },
            {
                'make': 'Hyundai',
                'model': 'Tucson',
                'year': 2023,
                'car_type': 'suv',
                'daily_rate': 55,
                'description': 'Modern SUV with great value and advanced safety features.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800'
            },
            {
                'make': 'Porsche',
                'model': '911',
                'year': 2023,
                'car_type': 'sports',
                'daily_rate': 200,
                'description': 'Legendary sports car with unmatched performance and handling.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1607853202273-797f1c22a38e?w=800'
            },
            {
                'make': 'Lexus',
                'model': 'RX',
                'year': 2023,
                'car_type': 'luxury',
                'daily_rate': 95,
                'description': 'Luxury SUV with exceptional reliability and comfort.',
                'available': True,
                'image_url': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800'
            }
        ]

        # Create cars with images
        for car_data in cars_data:
            car, created = Car.objects.get_or_create(
                make=car_data['make'],
                model=car_data['model'],
                year=car_data['year'],
                defaults={
                    'car_type': car_data['car_type'],
                    'daily_rate': car_data['daily_rate'],
                    'description': car_data['description'],
                    'available': car_data['available']
                }
            )
            
            if created:
                # Download and save the image
                try:
                    response = requests.get(car_data['image_url'])
                    if response.status_code == 200:
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(response.content)
                        img_temp.flush()
                        
                        # Generate a filename
                        filename = f"{car_data['make']}_{car_data['model']}_{car_data['year']}.jpg"
                        car.image.save(filename, File(img_temp), save=True)
                        self.stdout.write(self.style.SUCCESS(f'Successfully created car: {car}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Could not download image for {car}: {str(e)}'))

        # Create a sample driver user if it doesn't exist
        driver_user, created = User.objects.get_or_create(
            username='driver1',
            defaults={
                'email': 'driver1@example.com',
                'first_name': 'John',
                'last_name': 'Driver'
            }
        )
        
        if created:
            driver_user.set_password('driverpass123')
            driver_user.save()
            
            Driver.objects.create(
                user=driver_user,
                license_number='DRV123456',
                is_available=True
            )
            self.stdout.write(self.style.SUCCESS('Successfully created sample driver'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data')) 