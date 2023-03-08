import datetime

import pytz
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Image, ImageToken
from .serializers import (ExpirationTimeSerializer, ImageSerializer,
                          ImageTokenSerializer, ThumbnailCreateSerializer)


class ImageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = ImageSerializer

    def get_queryset(self):
        user = self.request.user
        self.queryset = Image.objects.filter(author=user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save()
        for height in self.request.user.plan.thumbnail_sizes:
            original_image = serializer.instance.pk
            thumbnail_serializer = ThumbnailCreateSerializer(
                data={
                    "height": height,
                    "original_image": original_image,
                }
            )
            if thumbnail_serializer.is_valid():
                thumbnail_serializer.save()

    @action(detail=True, methods=["post"], serializer_class=ExpirationTimeSerializer)
    def get_expiring_url(self, request, pk):

        if not request.user.plan.expiring_image_access:
            return Response({"detail": "You don't have permission to this action"}, status=status.HTTP_403_FORBIDDEN)

        time_serializer = self.get_serializer_class()(data=request.data)
        if time_serializer.is_valid():
            expiration_seconds = time_serializer.data["expiration_seconds"]
        else:
            return Response(time_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image = self.get_object()
        utc_now = timezone.now().replace(tzinfo=pytz.utc)
        expiration_date = utc_now + datetime.timedelta(0, expiration_seconds)
        data = {"original_image": image.pk, "expiration_date": expiration_date}
        token_serializer = ImageTokenSerializer(data=data)
        if token_serializer.is_valid():
            token_serializer.save()
        else:
            return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        url = reverse("images:expiring-image")
        token = str(token_serializer.instance.token)
        domain = get_current_site(request)
        return Response("http://" + str(domain) + f"{url}?token={token}")


class ExpiringImageUrl(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        token = request.GET.get("token")
        token_instance = get_object_or_404(ImageToken, token=token)
        if token_instance.expiration_date < timezone.now().replace(tzinfo=pytz.utc):
            content = {"Temporary image": "Time expired"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        image = get_object_or_404(Image, token=token)
        response = HttpResponse(image.file, content_type="image/jpeg")
        return response