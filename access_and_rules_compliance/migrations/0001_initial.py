# Generated by Django 3.2 on 2024-09-03 14:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Law',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('publish_date', models.DateField(default=django.utils.timezone.now)),
                ('language', models.CharField(choices=[('English', 'English'), ('Romanian', 'Romanian')], default='Romanian', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='LawCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, editable=False, max_length=100)),
            ],
            options={
                'verbose_name': 'Law Document',
                'verbose_name_plural': 'Law Documents',
            },
        ),
    ]