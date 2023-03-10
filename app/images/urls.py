from django.urls import include, path
from rest_framework import routers

from .views import ExpiringImageUrl, ImageViewSet

app_name = "images"

router = routers.SimpleRouter()
router.register("images", ImageViewSet, basename='image')


urlpatterns = [
    path("", include(router.urls)),
    path('images/temporary', ExpiringImageUrl.as_view(), name='expiring-image'),
]

