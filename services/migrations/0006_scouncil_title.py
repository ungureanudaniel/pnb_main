# Generated by Django 4.2 on 2023-06-20 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_rename_expert_scouncil_interest_scouncil_interest_de_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scouncil',
            name='title',
            field=models.CharField(default='Dr.', max_length=20),
            preserve_default=False,
        ),
    ]
