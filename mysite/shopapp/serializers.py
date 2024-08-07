from .models import Product, Tag, ProductImage, Sales, Review, ProductSpecification, Order
from catalog.serializers import ImageSerializers, TagsSerializers
from basket.serializers import BasketSerializers
from rest_framework import serializers


class ProductSpecificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ("name", "value", )


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("author", "email", "text", "rate", "date",)


class ProductDetailsSerializers(serializers.ModelSerializer):
    images = ImageSerializers(many=True, required=False)
    tags = TagsSerializers(many=True, required=False)
    specifications = ProductSpecificationSerializers(many=True)
    reviews = ReviewSerializers(many=True)

    class Meta:
        model = Product
        fields = ("id",
                  "category", "price", "count", "date",
                  "title", "description", "freeDelivery", "images", "tags", 'reviews', "rating", "specifications",
                  "reviews")


class ReviewDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("author", "email", "text", "rate", "date", "product")

    def create(self, validated_data):
        return Review.objects.create(**validated_data)



class OrderSerializers(serializers.ModelSerializer):
    product = BasketSerializers(many=True)
    class Meta:
        model = Order
        fields = ('createdAt',
                  'fullName',
                  'email',
                  'phone',
                  'deliveryType',
                  'paymentType', 'totalCost', 'status', 'city', 'address', 'product', 'profile')

