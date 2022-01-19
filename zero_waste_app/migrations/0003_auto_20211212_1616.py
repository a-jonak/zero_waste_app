# Generated by Django 3.2.10 on 2021-12-12 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zero_waste_app', '0002_auto_20211128_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='productlist',
            name='number',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(help_text='Enter your desired user name', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='Enter password', max_length=50),
        ),
    ]