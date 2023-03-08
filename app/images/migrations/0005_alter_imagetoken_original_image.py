# Generated by Django 4.1.7 on 2023-03-08 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_imagetoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagetoken',
            name='original_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token', to='images.image'),
        ),
    ]
