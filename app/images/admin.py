from django.contrib import admin

from .models import Image, ImageToken, Thumbnail


class ImageAdmin(admin.ModelAdmin):
    pass


class ImageTokenAdmin(admin.ModelAdmin):
    pass


class ThumbnailAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageToken, ImageTokenAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)
