# Generated by Django 4.1.11 on 2023-12-05 10:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0021_remove_vehiclecategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowedvehicles',
            name='permit_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='allowedvehicles',
            name='permit_nr',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]