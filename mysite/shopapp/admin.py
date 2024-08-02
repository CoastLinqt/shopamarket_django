from django.contrib import admin
from .models import Tag,Product, ProductImage, ProductSpecification, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("pk", "title", 'description', "price", "count",
                    "date", "freeDelivery", "limited", "active", "category", "rating")

    exclude = ('rating',)

    list_display_links = "pk", "title"
    ordering = "pk", "title"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "pk", "name",
    list_display_links = "pk", "name"
    ordering = "pk", "name"


@admin.register(ProductImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "product"
    list_display_links = "pk", "name", "product"
    ordering = "pk", "name", "product"


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "value"
    list_display_links = "pk", "name", "value"
    ordering = "pk", "name", "value"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "pk", "author", "email", "text", "rate", "date", "product"
    list_display_links = "pk", "author", "email"
    ordering = "pk", "author"