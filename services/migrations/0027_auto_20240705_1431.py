# Generated by Django 3.2 on 2024-07-05 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0026_auto_20240607_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allowedvehicles',
            name='area',
        ),
        migrations.AddField(
            model_name='allowedvehicles',
            name='area',
            field=models.ManyToManyField(blank=True, related_name='allowed_vehicles', to='services.AccessArea'),
        ),
    ]