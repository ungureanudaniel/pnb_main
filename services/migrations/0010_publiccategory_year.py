# Generated by Django 3.2 on 2023-03-27 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_auto_20230327_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='publiccategory',
            name='year',
            field=models.IntegerField(default='2022'),
            preserve_default=False,
        ),
    ]