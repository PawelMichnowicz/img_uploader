# Generated by Django 4.1.7 on 2023-03-05 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thumbnail',
            name='original_image',
        ),
    ]