
# urls.py
from django.urls import path,include
from . import views

app_name = 'diet'
urlpatterns = [
    path('food_types/', views.list_food_types, name='list_food_types'),
    path('food/', views.get_food_list, name='food_list'),
    path('create/', views.create_meal, name='create_meal'),
    path('', views.get_meal_list, name='meal_list'),
    path('<int:meal_id>/', views.get_meal, name='meal_detail'),
    # path('<str:food_name>/', views.get_meal, name='meal_by_food_name'),
    path('<int:meal_id>/update/', views.update_meal, name='update_meal'),
    path('<int:meal_id>/delete/', views.delete_meal, name='meal_delete'),
    path('calorie-info/', views.get_calorie_info, name='get_calorie_info'),
    # path('', include('diet.formss.urls')),
]










