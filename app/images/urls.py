from django.urls import include, path
from rest_framework import routers

from .views import ImageViewSet

app_name = "images"

router = routers.SimpleRouter()
router.register("images", ImageViewSet)


urlpatterns = [
    path("", include(router.urls)),
    ]