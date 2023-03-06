from rest_framework.serializers import ModelSerializer
import re
import os
from .models import Image
from django.core.files import File
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from imagekit import ImageSpec
from imagekit.processors import ResizeToFit
from rest_framework import serializers

from .models import Image, Thumbnail


class ThumbnailGenerator(ImageSpec):
    def __new__(cls, source, height):
        cls.processors = [ResizeToFit(height=height)]
        return super().__new__(cls)

    def __init__(self, source, height):
        super().__init__(source)


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ["author", "creation_time", "file"]


class ThumbnailSerializer(ModelSerializer):
    domain = serializers.CharField(read_only=True)

    class Meta:
        model = Thumbnail
        fields = ["original_image", "height", "file", "domain"]

    def create(self, validated_data):
        thumbnail_generator = ThumbnailGenerator(
            source=validated_data["original_image"].file,
            height=validated_data["height"],
        )
        thumbnail = thumbnail_generator.generate()

        filename, extension = validated_data["original_image"].file.name.split(".")
        temporary_file = filename + f"_{validated_data['height']}px.{extension}"
        f = open(temporary_file, "wb+")
        f.write(thumbnail.read())
        validated_data["file"] = File(f)
        instance = super().create(validated_data)
        os.remove(temporary_file)

        return instance
