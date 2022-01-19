# Generated by Django 3.2.9 on 2022-01-06 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zero_waste_app', '0008_alter_productinstance_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('unit', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='productinstance',
            options={'permissions': (('can_add_new_product', 'Add new product'), ('can_add_existing_product', 'Add product'), ('can_delete_product', 'Delete product'))},
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zero_waste_app.product')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zero_waste_app.recipe')),
            ],
        ),
    ]