# Generated by Django 3.2 on 2023-05-30 05:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20230530_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 30, 5, 49, 18, 948952, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='expiry',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 28, 5, 49, 18, 947953, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 30, 5, 49, 18, 947953, tzinfo=utc)),
        ),
    ]