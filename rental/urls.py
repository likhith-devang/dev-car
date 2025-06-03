from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/<int:car_id>/edit/', views.car_edit, name='car_edit'),
    path('cars/<int:car_id>/rent/', views.create_rental, name='create_rental'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('rentals/<int:rental_id>/cancel/', views.cancel_rental, name='cancel_rental'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
] 