# Generated by Django 3.2.9 on 2022-01-06 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zero_waste_app', '0009_auto_20220106_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='unit',
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='unit',
            field=models.TextField(default=0),
        ),
    ]