# Generated by Django 4.2.2 on 2023-10-03 08:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0070_alter_payment_price_alter_payment_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 3, 8, 6, 29, 896838, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='expiry',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 1, 1, 8, 6, 29, 893840, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 10, 3, 8, 6, 29, 893840, tzinfo=datetime.timezone.utc)),
        ),
    ]