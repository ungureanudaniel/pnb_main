# Generated by Django 3.2 on 2023-03-27 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_publiccatlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='publiccatlink',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='services.publiccategory'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publiccatlink',
            name='link_ro',
            field=models.FileField(blank=True, max_length=254, null=True, upload_to='public_docs/%d_%b_%Y/'),
        ),
    ]