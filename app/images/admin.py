from django.contrib import admin
from .models import Image, Thumbnail


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)


class ThumbnailAdmin(admin.ModelAdmin):
    pass


admin.site.register(Thumbnail, ThumbnailAdmin)
