from django.db import models
from django.contrib.auth import get_user_model

# def upload_to():


class Image(models.Model):
    filename = models.CharField(max_length=40)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="images"
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(upload_to='images_files')


