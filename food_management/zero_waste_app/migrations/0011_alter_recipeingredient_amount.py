# Generated by Django 3.2.9 on 2022-01-06 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zero_waste_app', '0010_auto_20220106_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.FloatField(),
        ),
    ]
