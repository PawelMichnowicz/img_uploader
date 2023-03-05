# Generated by Django 4.1.7 on 2023-03-05 14:16

from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_alter_image_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='thumbnail',
            name='file',
            field=models.ImageField(blank=True, upload_to=images.models.upload_to),
        ),
    ]
