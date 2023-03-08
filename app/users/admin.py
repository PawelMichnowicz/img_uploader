from django.contrib import admin

from .models import Plan, User


class PlanAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Plan, PlanAdmin)
admin.site.register(User, UserAdmin)
