# Generated by Django 4.1.7 on 2023-03-24 08:48

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attraction',
            name='name_de',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='attraction',
            name='name_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='attraction',
            name='name_ro',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='attraction',
            name='text_de',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='attraction',
            name='text_en',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='attraction',
            name='text_ro',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='attractioncategory',
            name='name_de',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='attractioncategory',
            name='name_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='attractioncategory',
            name='name_ro',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='text_de',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='text_en',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='text_ro',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='title_de',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='title_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='title_ro',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='blogpostcategory',
            name='title_de',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='blogpostcategory',
            name='title_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='blogpostcategory',
            name='title_ro',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='text_de',
            field=ckeditor.fields.RichTextField(max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='text_en',
            field=ckeditor.fields.RichTextField(max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='text_ro',
            field=ckeditor.fields.RichTextField(max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='title_de',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='title_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='title_ro',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='publiccategory',
            name='text_de',
            field=ckeditor.fields.RichTextField(max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='publiccategory',
            name='text_en',
            field=ckeditor.fields.RichTextField(max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='publiccategory',
            name='text_ro',
            field=ckeditor.fields.RichTextField(max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='publiccategory',
            name='title_de',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='publiccategory',
            name='title_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='publiccategory',
            name='title_ro',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='job_de',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='job_en',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='job_ro',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='text_de',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='text_en',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='text_ro',
            field=models.TextField(max_length=300, null=True),
        ),
    ]