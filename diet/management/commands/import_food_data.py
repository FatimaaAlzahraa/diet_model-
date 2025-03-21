import csv
from django.core.management.base import BaseCommand
from diet.models import Food
from decimal import Decimal
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Import food data from the nutrition.csv into the Food model'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join(settings.BASE_DIR, 'diet/data')
        csv_file_path = os.path.join(data_dir, 'nutrition.csv')

        def clean_value(value):
            if value:
                try:
                    return Decimal(value.replace(' g', '').replace(' mg', '').replace('ml', '').strip())
                except ValueError:
                    return Decimal('0.0')
            return Decimal('0.0')

        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Create or update the food item
                food, created = Food.objects.get_or_create(
                    name=row['name'],
                    defaults={
                        'calories': clean_value(row['calories']),
                        'fat': clean_value(row['fat']),
                        'carbohydrates': clean_value(row['carbohydrate']),
                        'protein': clean_value(row['protein']),
                        'portion_size': Decimal('100'),  # Default portion size is 100g
                    }
                )
                if not created:  # If the food already exists, we update it
                    food.calories = clean_value(row['calories'])
                    food.fat = clean_value(row['fat'])
                    food.carbohydrates = clean_value(row['carbohydrate'])
                    food.protein = clean_value(row['protein'])
                    food.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported food data into the Food model'))
