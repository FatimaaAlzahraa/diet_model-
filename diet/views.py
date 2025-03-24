# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum
from django.utils import timezone
from decimal import Decimal
from drf_yasg.utils import swagger_auto_schema
from .models import Food, Meal , StepHistory
from django.utils import timezone
from .serializers import FoodSerializer, MealSerializer , StepHistorySerializer

# 1- Retrieve a list of all available meal types
@swagger_auto_schema(method='get', responses={200: 'List of available meal types'})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_food_types(request):
    """Retrieve a list of all available meal types."""
    
    meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    return Response({"meal_types": meal_types}, status=status.HTTP_200_OK)


# 2- Retrieve a list of all available foods, with optional search query
@swagger_auto_schema(method='get', responses={200: FoodSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_food_list(request):
    """Retrieve a list of all available foods, with an optional search query."""
    
    search_query = request.GET.get('search', '').strip()  
    
    if search_query:
        foods = Food.objects.filter(Q(name__icontains=search_query))
    else:
        foods = Food.objects.all()

    serializer = FoodSerializer(foods, many=True)
    return Response({"foods": serializer.data}, status=status.HTTP_200_OK)


# 3- Create a new meal
@swagger_auto_schema(method='post', request_body=MealSerializer, responses={201: MealSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_meal(request):
    """Create a new meal by selecting a food and specifying a portion size."""
    
    data = request.data  

    if 'food_name' not in data:
        return Response({'error': 'Food name is required.'}, status=status.HTTP_400_BAD_REQUEST)

    food_name = data['food_name'].strip()

    try:
        food = Food.objects.get(name__iexact=food_name)
    except Food.DoesNotExist:
        return Response({'error': 'Food not found.'}, status=status.HTTP_400_BAD_REQUEST)

    portion_size = data.get('portion_size', 100)
    meal_type = data.get('meal_type', 'snack').strip()

    if meal_type not in ['breakfast', 'lunch', 'dinner', 'snack']:
        return Response({'error': 'Invalid meal type. Choose one of: breakfast, lunch, dinner, snack.'}, status=status.HTTP_400_BAD_REQUEST)

    meal = Meal.objects.create(
        user=request.user,
        food_name=food,
        meal_type=meal_type,
        portion_size=portion_size,
    )

    meal.calculate_nutrition()
    meal.save()

    serializer = MealSerializer(meal)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# 4- Retrieve all meals for the authenticated user, grouped by meal type
@swagger_auto_schema(method='get', responses={200: "Meals grouped by meal type"})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meal_list(request):
    """Retrieve all meals for the authenticated user, grouped by meal type."""
    
    meals = Meal.objects.filter(user=request.user)
    
    meal_groups = {
        "breakfast": [],
        "lunch": [],
        "dinner": [],
        "snack": []
    }

    for meal in meals:
        meal_data = {
            "id": meal.meal_id,
            "food_name": meal.food_name.name,
            "portion_size": meal.portion_size,
            "calories": meal.calories,
            "protein":meal.protein,
            "carbohydrates":meal.carbohydrates,
            "fat":meal.fat,
            "sugars":meal.sugars,
        }
        meal_groups[meal.meal_type].append(meal_data)

    return Response(meal_groups, status=status.HTTP_200_OK)


# 5- Retrieve the details of a single meal by meal_id or food name
@swagger_auto_schema(method='get', responses={200: MealSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meal(request, meal_id ):
    meal = Meal.objects.get(meal_id=meal_id, user=request.user)
    serializer = MealSerializer(meal, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
    # """Retrieve the details of a single meal by its food name or meal_id."""

    # if food_name:
    #     meals = Meal.objects.filter(user=request.user, food_name__name__iexact=food_name)
    # elif meal_id:
    #     try:
    #         meal = Meal.objects.get(meal_id=meal_id, user=request.user)

    #     except Meal.DoesNotExist:
    #         return Response({"error": "Meal not found."}, status=status.HTTP_404_NOT_FOUND)
    # else:
    #     return Response({"error": "Either 'meal_id' or 'food_name' must be provided."}, status=status.HTTP_400_BAD_REQUEST)

    # serializer = MealSerializer(meal, many=True)
    # return Response(serializer.data, status=status.HTTP_200_OK)


# 6- Retrieve the list of foods consumed grouped by day.  
@swagger_auto_schema(method='get', responses={200: MealSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_foods_by_day(request):
    """Retrieve the list of foods consumed by the authenticated user, grouped by day."""
    
    # Get the 'date' query parameter, if provided
    date_str = request.GET.get('date', None)
    if date_str:
        try:
            # Parse the date string to a datetime object
            date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # If no date is provided, default to today's date
        date = timezone.now().date()
    
    # Fetch meals for the specific date
    meals = Meal.objects.filter(user=request.user, date=date)
    
    # Group meals by meal type
    meal_groups = {
        "breakfast": [],
        "lunch": [],
        "dinner": [],
        "snack": []
    }

    for meal in meals:
        meal_data = {
            "id": meal.meal_id,
            "food_name": meal.food_name.name,
            "portion_size": meal.portion_size,
            "calories": meal.calories,
            "protein": meal.protein,
            "carbohydrates": meal.carbohydrates,
            "fat": meal.fat,
            "sugars": meal.sugars,
        }
        meal_groups[meal.meal_type].append(meal_data)

    return Response(meal_groups, status=status.HTTP_200_OK)

# 7- Update an existing meal
@swagger_auto_schema(method='put', request_body=MealSerializer, responses={200: MealSerializer})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_meal(request, meal_id):
    """Update an existing meal."""
    
    data = request.data
    food_name = data.get('food_name', '').strip()

    try:
        food_instance = Food.objects.get(name__iexact=food_name)
    except Food.DoesNotExist:
        return Response({"error": "Food not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        meal = Meal.objects.get(meal_id=meal_id, user=request.user)
    except Meal.DoesNotExist:
        return Response({"error": "Meal not found."}, status=status.HTTP_404_NOT_FOUND)

    meal.food_name = food_instance
    meal.portion_size = data.get('portion_size', meal.portion_size)
    
    meal.calculate_nutrition()
    meal.save()
    
    serializer = MealSerializer(meal)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 8- Delete an existing meal
@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_meal(request, meal_id):
    """Delete an existing meal."""
    
    try:
        meal = Meal.objects.get(meal_id=meal_id, user=request.user)
        meal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Meal.DoesNotExist:
        return Response({"error": "Meal not found."}, status=status.HTTP_404_NOT_FOUND)

#9. Create an API to receive step data from the fluter app:
@swagger_auto_schema(method='post', request_body=StepHistorySerializer, responses={201: StepHistorySerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_steps(request):
    """Record the steps taken by the user and calculate calories burned."""
    
    data = request.data
    steps = data.get('steps')

    if steps is None:
        return Response({'error': 'Steps are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create StepHistory object
    step_history = StepHistory.objects.create(
        user=request.user,
        steps=steps,
    )

    # Return the created object with calories burned
    serializer = StepHistorySerializer(step_history)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

#10.an API to view your step history and calories burned:
@swagger_auto_schema(method='get', responses={200: StepHistorySerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_step_history(request):
    """Retrieve the history of steps and calories burned by the user."""
    
    # Fetch step history for the authenticated user
    step_history = StepHistory.objects.filter(user=request.user).order_by('-date')

    serializer = StepHistorySerializer(step_history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 11- Retrieve calorie info (total consumed and remaining for the day)
@swagger_auto_schema(method='get', responses={200: 'Total calories consumed, burned, and remaining for the day.'})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_calorie_info(request):
    """Retrieve the total calories consumed, burned, and remaining calories for the day."""
    
    # Get total calories consumed from meals
    total_calories_consumed = Meal.objects.filter(
        user=request.user, 
        date=timezone.now().date()
    ).aggregate(total_calories=Sum('calories'))['total_calories'] or Decimal('0.0')

    # Get total steps taken today
    total_steps = StepHistory.objects.filter(
        user=request.user, 
        date=timezone.now().date()
    ).aggregate(total_steps=Sum('steps'))['total_steps'] or 0
    
    # Calculate calories burned based on steps (0.04 calories per step as an example)
    calories_burned_from_steps = total_steps * 0.04  # Assuming 0.04 calories burned per step
    calories_burned_from_steps = Decimal(calories_burned_from_steps)
    
    # Get user's daily calorie goal from profile
    user_profile = request.user.profile
    daily_calorie_goal = user_profile.daily_calorie_goal  # Automatically calculated in profile
    
    # Calculate remaining calories: goal - consumed + burned calories
    remaining_calories = daily_calorie_goal - total_calories_consumed + calories_burned_from_steps

    # Prepare the response with all relevant calorie information
    return Response({
        'calorie_goal': str(daily_calorie_goal),  # Daily calorie goal
        'total_calories_consumed': str(total_calories_consumed),  # Total calories consumed today
        'calories_burned_from_steps': str(calories_burned_from_steps),  # Calories burned from steps
        'remaining_calories': str(remaining_calories),  # Remaining calories for the day
    }, status=status.HTTP_200_OK)