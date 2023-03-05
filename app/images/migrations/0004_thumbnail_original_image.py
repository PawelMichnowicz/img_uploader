# Generated by Django 4.1.7 on 2023-03-05 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_remove_thumbnail_original_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='thumbnail',
            name='original_image',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='images.image'),
            preserve_default=False,
        ),
    ]
