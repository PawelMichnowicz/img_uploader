import os
from django.core.exceptions import ValidationError


def check_file_size(value):
    limit = 25 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Maximum size is equal 25MB")