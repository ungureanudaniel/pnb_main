# Generated by Django 4.2.2 on 2023-09-17 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_parkregulationcategory_text_de_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wildlife',
            name='weight_max',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=4),
            preserve_default=False,
        ),
    ]