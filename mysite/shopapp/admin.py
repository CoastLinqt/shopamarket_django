from django.contrib import admin
from .models import Tag,Product, ProductImage, ProductSpecification, Review, Order, Payment



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("pk", "number", "name", "month", "year", "code", "order")

    list_display_links = "pk", "number"

    ordering = "pk",


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ("pk", "createdAt", 'fullName', "email", "phone",
                    "deliveryType", "paymentType", "totalCost", "status", "city", "address")


    list_display_links = "pk", "fullName"
    ordering = "pk", "fullName"


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