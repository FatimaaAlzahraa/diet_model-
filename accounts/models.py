from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
