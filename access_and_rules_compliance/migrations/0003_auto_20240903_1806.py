# Generated by Django 3.2 on 2024-09-03 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access_and_rules_compliance', '0002_law_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawcategory',
            name='name_de',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='lawcategory',
            name='name_en',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='lawcategory',
            name='name_ro',
            field=models.CharField(max_length=50, null=True),
        ),
    ]