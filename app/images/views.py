from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .models import Image
from .serializers import ImageSerializer

class ImageViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    serializer_class = ImageSerializer
    queryset = Image.objects.all()