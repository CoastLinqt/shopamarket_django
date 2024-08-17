from .models import Categories
from rest_framework import serializers
from shopapp.models import Sales
from shopapp.models import Product, ProductImage, Tag
from django.db.models import Avg, Count
from django.core.validators import MinValueValidator, MaxValueValidator


class SubSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = ["id", "title", "image"]

    def get_image(self, obj):
        return {
            "src": obj.image.url,
            "alt": obj.image.name,
        }


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubSerializer(many=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = ["id", "title", "image", "subcategories"]

    def get_image(self, obj):
        return {
            "src": obj.image.url,
            "alt": obj.image.name,
        }


class ImageSerializers(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()
    alt = serializers.CharField(default="pictures")

    class Meta:
        model = ProductImage
        fields = "src", "alt"

    def get_src(self, obj):
        if obj.image:
            return obj.image.url
        return None


class TagsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class CatalogProductSerializers(serializers.ModelSerializer):
    images = ImageSerializers(many=True, required=False)
    tags = TagsSerializers(many=True, required=False)
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    price = serializers.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(100000000)],
    )

    class Meta:
        model = Product
        fields = (
            "pk",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )

    def get_rating(self, obj):
        avg = obj.reviews.aggregate(Avg("rate"))

        if avg["rate__avg"] is not None:
            return round(avg["rate__avg"], 2)
        return 0

    def get_reviews(self, obj):
        count = obj.reviews.aggregate(Count("pk"))
        result = count["pk__count"]

        if result is not None:
            return result
        return 0


class SalesSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    dateFrom = serializers.DateTimeField(format="%d-%m-%Y")
    dateTo = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = Sales
        fields = ("pk", "salePrice", "dateFrom", "dateTo", "title", "price", "images")

    def get_title(self, obj):
        return obj.product.title

    def get_price(self, obj):
        return obj.product.price

    def get_images(self, obj):
        return [{"src": obj.images.image.url, "alt": obj.images.image.name}]
