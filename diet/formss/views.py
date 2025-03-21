
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Meal,Food
from .forms import MealForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

# View for selecting meal type
@login_required
def select_meal_type(request):
    """Select meal type (Breakfast, Lunch, Dinner, Snack)."""
    meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    return render(request, 'diet/select_meal_type.html', {'meal_types': meal_types})


# View for selecting food based on meal type
@login_required
# views.py
def select_food(request):
    """Allow the user to select a food item based on the meal type."""
    meal_type = request.GET.get('meal_type')
    
    if meal_type not in ['breakfast', 'lunch', 'dinner', 'snack']:
        return HttpResponseRedirect(reverse('diet:select_meal_type'))
    
    foods = Food.objects.filter(meal_type=meal_type)  # Now this will work because the field exists
    
    return render(request, 'diet/select_food.html', {'foods': foods, 'meal_type': meal_type})


# View for creating a meal
@login_required
# views.py
def create_meal(request):
    """Create a new meal by selecting a food item and specifying a portion size."""
    food_id = request.GET.get('food_id')
    meal_type = request.GET.get('meal_type')
    
    try:
        food = Food.objects.get(id=food_id)
    except Food.DoesNotExist:
        return HttpResponseRedirect(reverse('diet:select_food'))

    # If the form is submitted to create the meal
    if request.method == 'POST':
        portion_size = request.POST.get('portion_size', 100)
        meal_date = request.POST.get('date', timezone.now().date())
        meal_time = request.POST.get('time', timezone.now().time())
        
        # Create the meal instance
        meal = Meal.objects.create(
            user=request.user,
            food_name=food,
            meal_type=meal_type,
            portion_size=portion_size,
            date=meal_date,
            time=meal_time
        )
        
        # Recalculate nutrition
        meal.calculate_nutrition()
        meal.save()

        return HttpResponseRedirect(reverse('diet:meal_detail', kwargs={'meal_id': meal.meal_id}))

    return render(request, 'diet/create_meal.html', {'food': food, 'meal_type': meal_type})


# View for meal detail
@login_required
# views.py
def meal_detail(request, meal_id):
    """Display the details of a single meal including calories and nutrition."""
    try:
        meal = Meal.objects.get(meal_id=meal_id, user=request.user)
    except Meal.DoesNotExist:
        return HttpResponseRedirect(reverse('diet:meal_list'))
    
    return render(request, 'diet/meal_detail.html', {'meal': meal})


# View for updating a meal
@login_required
def update_meal(request, meal_id):
    """Update the details of an existing meal."""
    meal = get_object_or_404(Meal, meal_id=meal_id, user=request.user)
    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('diet:meal_detail', meal_id=meal.meal_id)
    else:
        form = MealForm(instance=meal)
    return render(request, 'diet/create_meal.html', {'form': form})

# View for deleting a meal
@login_required
def meal_delete(request, meal_id):
    """Delete a specific meal."""
    meal = get_object_or_404(Meal, meal_id=meal_id, user=request.user)
    if request.method == 'POST':
        meal.delete()
        return redirect('diet:meal_list')
    return render(request, 'diet/meal_confirm_delete.html', {'meal': meal})

# View for listing all meals
@login_required
def meal_list(request):
    """Retrieve and display all meals for the authenticated user."""
    meals = Meal.objects.filter(user=request.user)
    return render(request, 'diet/meal_list.html', {'meals': meals})
