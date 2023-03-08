import uuid

from django.contrib.auth import get_user_model
from django.db import models


def upload_to(instance, filename):
    return "images/{filename}".format(filename=filename)


class Image(models.Model):
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="images"
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(upload_to=upload_to)


class Thumbnail(models.Model):

    original_image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="thumbnails"
    )
    height = models.IntegerField()
    file = models.ImageField(upload_to=upload_to, blank=True)


class ImageToken(models.Model):
    original_image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="token"
    )
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expiration_date = models.DateTimeField()
