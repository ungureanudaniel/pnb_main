# Generated by Django 4.1.11 on 2023-11-02 15:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0079_alter_payment_currency_alter_payment_timestamp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='quantity_kids',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 2, 15, 39, 7, 601051, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='expiry',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 1, 31, 15, 39, 7, 599053, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 2, 15, 39, 7, 599053, tzinfo=datetime.timezone.utc)),
        ),
    ]