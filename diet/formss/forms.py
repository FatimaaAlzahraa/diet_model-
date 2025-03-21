from django import forms
from ..models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_type', 'food_name', 'portion_size', 'date', 'time'] 

