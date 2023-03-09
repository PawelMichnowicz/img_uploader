import tempfile
from time import sleep
from urllib.request import urlopen

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient
from users.models import Plan


def create_client(plan):
    if isinstance(plan, str):
        plan_instance = Plan.objects.get(name=plan)
    else:
        plan_instance = plan

    data = {
        "username": "username_" + get_random_string(length=10),
        "password": "password_123",
        "plan": plan_instance,
    }
    user = get_user_model().objects.create_user(**data)
    user_client = APIClient()
    user_client.force_authenticate(user)
    return user_client


def upload_image(user_client, url):
    with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
        img = Image.new("RGB", (10, 10))
        img.save(image_file, format="JPEG")
        image_file.seek(0)
        payload = {"file": image_file}
        res = user_client.post(url, payload)
    return res


class ImageUploadTests(TestCase):
    def setUp(self):
        self.basic_client = create_client("Basic")
        self.premium_client = create_client("Premium")
        self.enterprise_client = create_client("Enterprise")
        self.url = reverse("images:image-list")

    def test_upload_image_basic_user(self):
        response = upload_image(self.basic_client, self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(200, response.data["thumbnails"][0])
        self.assertIsNone(response.data["original_image"])

        expiring_image_url = reverse(
            "images:image-get_expiring_url", args=[response.data["pk"]]
        )
        response_image_url = self.enterprise_client.post(
            expiring_image_url, {"expiration_seconds": "300"}
        )
        self.assertEqual(response_image_url.status_code, status.HTTP_404_NOT_FOUND)

    def test_upload_image_premium_user(self):
        response = upload_image(self.premium_client, self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(200, response.data["thumbnails"][0])
        self.assertIn(400, response.data["thumbnails"][1])
        self.assertIsNotNone(response.data["original_image"])

    def test_upload_image_enterprise_user(self):
        response = upload_image(self.enterprise_client, self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(200, response.data["thumbnails"][0])
        self.assertIn(400, response.data["thumbnails"][1])
        self.assertIsNotNone(response.data["original_image"])

        expiring_image_url = reverse(
            "images:image-get_expiring_url", args=[response.data["pk"]]
        )
        response_image_url = self.enterprise_client.post(
            expiring_image_url, {"expiration_seconds": "300"}
        )
        self.assertEqual(response_image_url.status_code, status.HTTP_200_OK)

        response_image_file = self.enterprise_client.get(response_image_url.data)
        self.assertIn(
            response_image_file.headers["Content-Type"], ["image/jpeg", "image/png"]
        )
        self.assertEqual(response_image_file.status_code, status.HTTP_200_OK)

    def test_upload_image_custom_plan_a(self):
        thumbnail_sizes = [100, 200, 300, 1000]
        plan_a = Plan.objects.create(
            name="plan_a",
            thumbnail_sizes=thumbnail_sizes,
            original_image_access=False,
            expiring_image_access=False,
        )
        client_a = create_client(plan_a)
        response_a = upload_image(client_a, self.url)

        self.assertIsNone(response_a.data["original_image"])
        for num, size in enumerate(thumbnail_sizes):
            self.assertIn(size, response_a.data["thumbnails"][num])

        expiring_image_url = reverse(
            "images:image-get_expiring_url", args=[response_a.data["pk"]]
        )
        response_image_url = client_a.post(
            expiring_image_url, {"expiration_seconds": "300"}
        )
        self.assertEqual(response_image_url.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_image_custom_plan_b(self):
        thumbnail_sizes = [100, 200, 300, 1000]
        plan_b = Plan.objects.create(
            name="plan_a",
            thumbnail_sizes=thumbnail_sizes,
            original_image_access=True,
            expiring_image_access=True,
        )
        client_b = create_client(plan_b)
        response_b = upload_image(client_b, self.url)

        self.assertIsNotNone(response_b.data["original_image"])
        for num, size in enumerate(thumbnail_sizes):
            self.assertIn(size, response_b.data["thumbnails"][num])

        expiring_image_url = reverse(
            "images:image-get_expiring_url", args=[response_b.data["pk"]]
        )
        response_image_url = client_b.post(
            expiring_image_url, {"expiration_seconds": "300"}
        )
        self.assertEqual(response_image_url.status_code, status.HTTP_200_OK)

        response_image_file = client_b.get(response_image_url.data)
        self.assertIn(
            response_image_file.headers["Content-Type"], ["image/jpeg", "image/png"]
        )
        self.assertEqual(response_image_file.status_code, status.HTTP_200_OK)
