# Generated by Django 4.1.7 on 2023-03-05 13:26

from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_thumbnail_original_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to=images.models.upload_to),
        ),
    ]