# Generated by Django 4.2.2 on 2023-07-04 08:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0030_alter_payment_timestamp_alter_ticket_expiry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 4, 8, 7, 14, 885365, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='expiry',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 10, 2, 8, 7, 14, 885365, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 4, 8, 7, 14, 885365, tzinfo=datetime.timezone.utc)),
        ),
    ]