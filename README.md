# Car Rental Application

A Django-based car rental application that allows users to browse, search, and rent cars with or without drivers.

## Features

- Browse available cars
- Search cars by make, model, or type
- View detailed car information
- Make rental reservations
- Option to include a driver
- User dashboard for managing rentals
- Admin interface for managing cars, drivers, and rentals

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd car-rental
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Load sample data:
```bash
python manage.py load_sample_data
```

7. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the admin interface at `http://127.0.0.1:8000/admin` to:
   - Add/edit cars
   - Manage drivers
   - View and manage rentals

2. Browse cars at `http://127.0.0.1:8000/cars/`

3. View car details and make reservations

4. Access your dashboard at `http://127.0.0.1:8000/dashboard/`

## Sample Accounts

- Admin: Use the superuser account you created
- Driver: 
  - Username: driver1
  - Password: driverpass123

## Technologies Used

- Django 5.1
- Bootstrap 5
- SQLite (can be changed to PostgreSQL/MySQL)
- Django Admin Interface 