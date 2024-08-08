from rest_framework import serializers
from django.contrib.auth.models import User
from shopapp.models import Product
from django.db.models import Avg, Count
from catalog.serializers import ImageSerializers, TagsSerializers
from django.core.validators import MinValueValidator, MaxValueValidator


class BasketSerializers(serializers.ModelSerializer):
    images = ImageSerializers(many=True, required=False)
    tags = TagsSerializers(many=True, required=False)
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("pk", "category",
                  "price", "count",
                  "date", "title", "description",
                  "freeDelivery", "images", "tags", "reviews", "rating")

    def get_count(self, obj):
        if not self.context:
            return obj.count

        count = self.context.get(f'{obj.pk}').get('count')
        return count


    def get_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rate'))

        if avg['rate__avg'] is not None:
            return round(avg['rate__avg'], 2)
        return 0

    def get_reviews(self, obj):

        count = obj.reviews.aggregate(Count('pk'))
        result = count['pk__count']

        if result is not None:
            return result
        return 0

    def get_price(self, obj):
        if not self.context:
            return obj.price
        result = obj.price * self.context.get(f'{obj.pk}').get('count')
        return result


class BasketFormSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField()
    count = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ("id", "count",)

