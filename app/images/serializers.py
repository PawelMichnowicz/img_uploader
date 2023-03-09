import os
import uuid

from django.contrib.sites.shortcuts import get_current_site
from django.core.files import File
from imagekit import ImageSpec
from imagekit.processors import ResizeToFit
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Image, ImageToken, Thumbnail


class ThumbnailGenerator(ImageSpec):
    def __new__(cls, source, height):
        cls.processors = [ResizeToFit(height=height)]
        return super().__new__(cls)

    def __init__(self, source, height):
        super().__init__(source)


class ThumbnailSerializer(ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = ["file"]

    def to_representation(self, instance):
        """Specify thumbnail sizes in your response"""
        data = super().to_representation(instance)
        data[instance.height] = data["file"]
        del data["file"]
        return data


class ImageSerializer(ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)
    original_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        fields = ["pk", "file", "original_image", "thumbnails"]
        extra_kwargs = {"file": {"write_only": True}}

    def get_original_image(self, obj):
        """Based on the user's plan, return a link to the original image or nothing at all"""
        if obj.author.plan.original_image_access:
            domain = get_current_site(self.context["request"])
            return "http://" + str(domain) + obj.file.url
        else:
            return None

    def create(self, validated_data):
        """Add request user as author when creating an image"""
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class ThumbnailCreateSerializer(ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = ["original_image", "height", "file"]

    def create(self, validated_data):
        """Create thumbnail from uploaded image"""
        thumbnail_generator = ThumbnailGenerator(
            source=validated_data["original_image"].file,
            height=validated_data["height"],
        )
        thumbnail = thumbnail_generator.generate()

        # create temporary image and overwrite it with output of thmubnail generator
        # include obtained file into validated_data and delete temporary image
        filename, extension = validated_data["original_image"].file.name.split(".")
        temporary_file = filename + f"_{validated_data['height']}px.{extension}"
        f = open(temporary_file, "wb+")
        f.write(thumbnail.read())
        validated_data["file"] = File(f)
        instance = super().create(validated_data)
        os.remove(temporary_file)

        return instance


class ExpirationTimeSerializer(serializers.Serializer):
    expiration_seconds = serializers.IntegerField(min_value=300, max_value=30000)


class ImageTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageToken
        fields = [
            "original_image",
            "token",
            "expiration_date",
        ]

    def create(self, validated_data):
        """Add generated token to the creation process"""
        validated_data["token"] = uuid.uuid4()
        return super().create(validated_data)
