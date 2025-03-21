# Generated by Django 4.2.16 on 2025-02-07 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("diet", "0002_remove_food_image_url_food_calories_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="food",
            old_name="portion_size",
            new_name="serving_size",
        ),
        migrations.RemoveField(
            model_name="food",
            name="carbohydrates",
        ),
        migrations.RemoveField(
            model_name="food",
            name="fat",
        ),
        migrations.RemoveField(
            model_name="food",
            name="protein",
        ),
    ]
