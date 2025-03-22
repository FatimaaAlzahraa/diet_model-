from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

# Create your models here.

suger_type_choises = (
    ('Type 1', 'Type 1'),
    ('Type 2', 'Type 2') ,
    ('Pre Diabetic','Pre Diabetic') ,
    ('genetic predisposition' ,'genetic predisposition' ),
    ('Normal' , 'Normal')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile' , default='default.jpeg')
    gender  = models.CharField(max_length=10 , choices=(('male', 'Male'), ('female', 'Female')))
    therapy =models.CharField(max_length=10 , choices=(('insulin', 'Insulin'), ('Tablets', 'Tablets')))
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    diabetes_type = models.CharField(max_length=22 , choices=suger_type_choises)
    age = models.IntegerField(null=True, blank=True)
    daily_calorie_goal = models.DecimalField(max_digits=7, decimal_places=2, default=2000.0)  # Default goal


    def __str__(self):
        return self.user.username
    
    def calculate_bmr(self):
        """Calculate BMR based on gender, weight, height, and age."""
        if self.gender == 'male':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        return bmr

    def calculate_daily_calorie_goal(self, activity_level='sedentary'):
        """Calculate the total daily calorie requirement based on activity level."""
        bmr = self.calculate_bmr()

        # Apply activity factor based on the activity level
        activity_factors = {
            'sedentary': 1.2,  # Little or no exercise
            'lightly_active': 1.375,  # Light exercise or sports 1-3 days a week
            'moderately_active': 1.55,  # Moderate exercise or sports 3-5 days a week
            'very_active': 1.725,  # Hard exercise or sports 6-7 days a week
        }

        # Default to 'sedentary' if no activity level is provided
        activity_factor = activity_factors.get(activity_level, 1.2)
        
        # Calculate the total daily calorie goal
        daily_calorie_goal = bmr * activity_factor
        return Decimal(daily_calorie_goal)

    # Automatically update the daily_calorie_goal when the profile is created or updated
    def save(self, *args, **kwargs):
        self.daily_calorie_goal = self.calculate_daily_calorie_goal()
        super().save(*args, **kwargs)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
