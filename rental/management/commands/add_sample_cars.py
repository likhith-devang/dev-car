from django.core.management.base import BaseCommand
from rental.models import Car
import requests
from django.core.files.base import ContentFile
import os

class Command(BaseCommand):
    help = 'Adds sample cars to the database'

    def handle(self, *args, **kwargs):
        # Sample car data
        cars_data = [
            {
                'make': 'Toyota',
                'model': 'Camry',
                'year': 2023,
                'car_type': 'sedan',
                'daily_rate': 50.00,
                'description': 'Comfortable and reliable sedan perfect for family trips and daily commuting.',
                'image_url': 'https://images.unsplash.com/photo-1617469767053-3c4f2a9c0459'
            },
            {
                'make': 'Honda',
                'model': 'CR-V',
                'year': 2023,
                'car_type': 'suv',
                'daily_rate': 65.00,
                'description': 'Spacious SUV with excellent fuel efficiency and modern features.',
                'image_url': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a'
            },
            {
                'make': 'BMW',
                'model': 'M4',
                'year': 2023,
                'car_type': 'sports',
                'daily_rate': 120.00,
                'description': 'High-performance sports car with stunning design and powerful engine.',
                'image_url': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8'
            },
            {
                'make': 'Mercedes-Benz',
                'model': 'S-Class',
                'year': 2023,
                'car_type': 'luxury',
                'daily_rate': 150.00,
                'description': 'Ultimate luxury sedan with cutting-edge technology and premium comfort.',
                'image_url': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8'
            },
            {
                'make': 'Tesla',
                'model': 'Model 3',
                'year': 2023,
                'car_type': 'sedan',
                'daily_rate': 80.00,
                'description': 'Electric sedan with impressive range and advanced autopilot features.',
                'image_url': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8'
            },
            {
                'make': 'Audi',
                'model': 'Q7',
                'year': 2023,
                'car_type': 'suv',
                'daily_rate': 90.00,
                'description': 'Premium SUV with quattro all-wheel drive and luxurious interior.',
                'image_url': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8'
            }
        ]

        for car_data in cars_data:
            # Create car object
            car = Car.objects.create(
                make=car_data['make'],
                model=car_data['model'],
                year=car_data['year'],
                car_type=car_data['car_type'],
                daily_rate=car_data['daily_rate'],
                description=car_data['description'],
                available=True
            )

            # Download and save image
            try:
                response = requests.get(car_data['image_url'])
                if response.status_code == 200:
                    image_name = f"{car_data['make']}_{car_data['model']}_{car_data['year']}.jpg"
                    car.image.save(image_name, ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f'Successfully added {car} with image'))
                else:
                    self.stdout.write(self.style.WARNING(f'Could not download image for {car}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error downloading image for {car}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Successfully added sample cars')) 