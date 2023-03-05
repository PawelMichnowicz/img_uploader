from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django.contrib.sites.shortcuts import get_current_site

from .models import Image
from .serializers import ImageSerializer, ThumbnailSerializer


class ImageViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    def perform_create(self, serializer):

        serializer.save()
        height = 200
        original_image = serializer.instance.pk
        current_domain = get_current_site(self.request)
        thumbnail_serializer = ThumbnailSerializer(data={'height':height, 'original_image':original_image, 'domain':current_domain})
        if thumbnail_serializer.is_valid():
            thumbnail_serializer.save()



