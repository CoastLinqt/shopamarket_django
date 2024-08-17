from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "fullName",
        "email",
        "phone",
    )
    list_display_links = "pk", "fullName"
    ordering = "pk", "fullName"
