# Generated by Django 3.2 on 2023-05-10 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0044_auto_20230509_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='email',
            field=models.EmailField(default='a', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='judet',
            field=models.CharField(choices=[('Brașov', 'Brașov'), ('Dâmbovița', 'Dâmbovița'), ('Prahova', 'Prahova')], default='Draft', max_length=10),
        ),
    ]