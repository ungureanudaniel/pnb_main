# Generated by Django 4.1.11 on 2024-01-17 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0020_allowedvehicles_area'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accessarea',
            name='slug',
        ),
    ]