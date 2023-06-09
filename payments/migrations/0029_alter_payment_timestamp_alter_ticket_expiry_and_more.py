# Generated by Django 4.2.1 on 2023-06-26 07:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0028_alter_payment_timestamp_alter_ticket_expiry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 26, 7, 56, 44, 620763, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='expiry',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 9, 24, 7, 56, 44, 619763, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 26, 7, 56, 44, 619763, tzinfo=datetime.timezone.utc)),
        ),
    ]
