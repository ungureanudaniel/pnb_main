# Generated by Django 4.2 on 2023-06-16 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='rank',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]