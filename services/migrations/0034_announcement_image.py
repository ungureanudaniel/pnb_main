# Generated by Django 3.2 on 2023-04-13 09:33

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0033_announcement_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, default='a', force_format='WebP', keep_meta=True, quality=75, scale=0.5, size=[640, None], upload_to='announcement_images'),
            preserve_default=False,
        ),
    ]