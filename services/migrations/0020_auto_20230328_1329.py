# Generated by Django 3.2 on 2023-03-28 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0019_alter_publiccatlink_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publiccategory',
            name='title',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='publiccategory',
            name='title_de',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='publiccategory',
            name='title_en',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='publiccategory',
            name='title_ro',
            field=models.CharField(max_length=70, null=True),
        ),
    ]