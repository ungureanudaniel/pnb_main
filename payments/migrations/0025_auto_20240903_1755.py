# Generated by Django 3.2 on 2024-09-03 14:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0024_auto_20240903_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 3, 14, 55, 15, 18106, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='expiry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 12, 2, 14, 55, 15, 18106, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 3, 14, 55, 15, 18106, tzinfo=utc)),
        ),
    ]