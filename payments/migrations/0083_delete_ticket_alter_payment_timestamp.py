# Generated by Django 4.1.11 on 2023-11-06 09:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0082_alter_payment_price_alter_payment_timestamp_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 6, 9, 8, 31, 876712, tzinfo=datetime.timezone.utc)),
        ),
    ]