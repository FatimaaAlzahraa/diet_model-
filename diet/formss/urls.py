# formss/urls.py
from django.urls import path
from . import views

# app_name = 'diet'

urlpatterns = [
    path('meals/select_type/', views.select_meal_type, name='select_meal_type'),  # Select meal type
    path('meals/select_food/', views.select_food, name='select_food'),  # Select food
    path('meal/create/', views.create_meal, name='create_meal'),  # Define meal_create view
    path('meal/detail/<int:meal_id>/', views.meal_detail, name='meal_detail'),  # View meal details
    path('meals/update/<int:meal_id>/', views.update_meal, name='update_meal'),  # Update meal
    path('meals/delete/<int:meal_id>/', views.meal_delete, name='meal_delete'),  # Delete meal
    path('meals/', views.meal_list, name='meal_list'),  # List all meals
]
