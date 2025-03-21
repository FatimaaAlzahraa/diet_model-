# diet/serializers.py

# diet/serializers.py

from rest_framework import serializers
from .models import Food, Meal

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name','portion_size','calories']

class MealSerializer(serializers.ModelSerializer):
    # Use SerializerMethodField to fetch the food name
    food_name = serializers.CharField(source='food_name.name')  # Get the food name
    class Meta:
        model = Meal
        fields = ['meal_id', 'meal_type', 'food_name', 'portion_size', 'calories', 'fat', 'carbohydrates', 'protein', 'sugars']


        