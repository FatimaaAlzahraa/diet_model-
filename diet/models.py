from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal
import os 
from django.conf import settings
import csv

class Food(models.Model):
    name = models.CharField(max_length=255)
    calories = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fat = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbohydrates = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    portion_size = models.DecimalField(max_digits=6, decimal_places=2, default=100)  # Default portion size in grams


    def __str__(self):
        return self.name
    

class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
    ]

    meal_id = models.AutoField(primary_key=True)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES, default='snack')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    food_name = models.ForeignKey(Food, on_delete=models.CASCADE)
    portion_size = models.DecimalField(max_digits=7, decimal_places=2)  # Portion size in grams
    calories = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    fat = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    carbohydrates = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    protein = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    sugars = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    calories_consumed = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)  # Track total calories consumed
    daily_calorie_goal = models.DecimalField(max_digits=7, decimal_places=2, default=2000.0)  # User's daily calorie goal
    calories_remaining = models.DecimalField(max_digits=7, decimal_places=2, default=2000.0)  # Remaining calories

    def __str__(self):
        return f"{self.food_name} ({self.meal_type})"

    def get_nutrition_data(self, food_name):
        """
        Retrieves the nutrition data for the given food name from the CSV file.
        """
        data_dir = os.path.join(settings.BASE_DIR, 'diet/data')  # Path to your data folder
        csv_file_path = os.path.join(data_dir, 'nutrition.csv')

        # Function to clean the numeric values
        def clean_value(value):
            if value:
                try:
                    # Remove non-numeric characters and return the value as Decimal
                    return Decimal(value.replace(' g', '').replace(' mg', '').replace('ml', '').strip())
                except ValueError:
                    return Decimal('0.0')  # If conversion fails, return 0.0
            return Decimal('0.0')

        try:
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['name'].lower() == food_name.lower():
                        return {
                            'calories': clean_value(row['calories']),
                            'fat': clean_value(row['fat']),
                            'carbohydrates': clean_value(row['carbohydrate']),
                            'protein': clean_value(row['protein']),
                            'sugars': clean_value(row['sugars']),
                        }
        except FileNotFoundError:
            return None

        return None

    def calculate_nutrition(self):
        """
        Calculate the nutrition values based on the portion size and food_name entered.
        """
        nutrition_data = self.get_nutrition_data(self.food_name.name)  # Get the nutrition data from the CSV
        if nutrition_data:
            portion_size = Decimal(str(self.portion_size))  # Ensure portion_size is a Decimal
            factor = portion_size / Decimal('100.0') # Portion size ratio over 100g
            self.calories = nutrition_data['calories'] * factor
            self.fat = nutrition_data['fat'] * factor
            self.carbohydrates = nutrition_data['carbohydrates'] * factor
            self.protein = nutrition_data['protein'] * factor
            self.sugars = nutrition_data['sugars'] * factor
             # Ensure both calories are in Decimal type for the += operation
            self.calories_consumed = Decimal(str(self.calories_consumed))  # Cast calories_consumed to Decimal
            self.calories_consumed += self.calories  # Add the calories of this meal to the total consumed  # Add the calories of this meal to the total consumed

    def save(self, *args, **kwargs):
        """Override the save method to calculate nutrition before saving."""
        self.calculate_nutrition()  # Calculate nutrition before saving
        # self.calories_remaining = self.daily_calorie_goal - self.calories_consumed  # Calculate remaining calories
        super().save(*args, **kwargs)
