# Generated by Django 4.2 on 2023-06-16 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0012_alter_payment_timestamp_alter_ticket_expiry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 16, 15, 42, 55, 222244, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='expiry',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 9, 14, 15, 42, 55, 221618, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 16, 15, 42, 55, 221597, tzinfo=datetime.timezone.utc)),
        ),
    ]