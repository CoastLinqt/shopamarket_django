from .models import Categories
from rest_framework import serializers
from shopapp.models import Sales
from shopapp.models import Product, ProductImage, Tag
from django.db.models import Avg, Count

class SubSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = ['id', 'title', 'image']

    def get_image(self, obj):
        return {
            'src': obj.image.url,
            'alt': obj.image.name,
        }

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubSerializer(many=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = ['id', 'title', 'image', 'subcategories']

    def get_image(self, obj):
        return {
            'src': obj.image.url,
            'alt': obj.image.name,
        }


class ImageSerializers(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()
    alt = serializers.CharField(default='pictures')

    class Meta:
        model = ProductImage
        fields = 'src', 'alt'

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

    class Meta:
        model = Product
        fields = ("pk",
                  "category", "price", "count", "date",
                  "title", "description", "freeDelivery", "images", "tags", 'reviews', "rating")

    def get_rating(self, obj):
        for i in obj.reviews.all():
            return i.rate

    def get_reviews(self, obj):
        for i in obj.reviews.all():
            return i.pk





class SalesSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    dateFrom = serializers.DateTimeField(format='%d-%m-%Y')
    dateTo = serializers.DateTimeField(format='%d-%m-%Y')

    class Meta:
        model = Sales
        fields = ("pk", "salePrice", "dateFrom", "dateTo", "title", "price", "images")

    def get_title(self, obj):
        return obj.product.title

    def get_price(self, obj):
        return obj.product.price

    def get_images(self, obj):

        return [{"src": obj.images.image.url,
                "alt": obj.images.image.name}]