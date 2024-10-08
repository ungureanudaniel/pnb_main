# Generated by Django 4.2.2 on 2023-09-17 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_wildlife'),
    ]

    operations = [
        migrations.AddField(
            model_name='wildlife',
            name='diet_de',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='diet_en',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='diet_ro',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='habitat_de',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='habitat_en',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='habitat_ro',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='name_de',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='name_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='name_ro',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='text_de',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='text_en',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='wildlife',
            name='text_ro',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='wildlife',
            name='height_max',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='wildlife',
            name='weight_max',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
