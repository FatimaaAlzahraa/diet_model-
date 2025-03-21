# Generated by Django 4.2.16 on 2025-02-09 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("diet", "0004_rename_serving_size_food_portion_size_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="food",
            name="meal_type",
            field=models.CharField(
                choices=[
                    ("breakfast", "Breakfast"),
                    ("lunch", "Lunch"),
                    ("dinner", "Dinner"),
                    ("snack", "Snack"),
                ],
                default="snack",
                max_length=10,
            ),
        ),
    ]
