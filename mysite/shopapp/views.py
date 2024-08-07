from rest_framework.views import APIView
from .models import Product, Tag, Order
from rest_framework.response import Response
from catalog.serializers import TagsSerializers
from .serializers import ProductDetailsSerializers, ReviewDetailsSerializers, OrderSerializers
from rest_framework import status
from basket.serializers import BasketSerializers
from basket.service import Cart
from django.db.models import Avg, Count


class ProductDetailView(APIView):
    def get(self, request, pk):

        queryset = Product.objects.filter(pk=pk)
        serialized = ProductDetailsSerializers(queryset, many=True)

        return Response(serialized.data[0])


class ProductDetailReviewView(APIView):
    def post(self, request, pk):
        data_dict = {}
        author = request.data['author']
        email = request.data['email']
        text = request.data['text']
        rate = request.data['rate']
        product = pk
        data_dict.update(author=author, email=email, text=text, rate=rate, product=product)

        serialized = ReviewDetailsSerializers(data=data_dict)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)

        return Response(serialized.errors, status.HTTP_400_BAD_REQUEST)


class TagsView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serialized = TagsSerializers(tags, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class OrderPostView(APIView):

    def post(self, request):
        cart = Cart(request)
        if request.user.is_authenticated and request.user.profile.user_id == request.user.pk:

            product_id = [product for product in cart.cart.keys()]

            queryset = (
                Product.objects.filter(pk__in=product_id)
                .prefetch_related("reviews")
                .annotate(rate=Avg("reviews__rate"), product_count=Count("reviews__pk"))
            )

            serialized = BasketSerializers(queryset, many=True, context=cart.cart)

            rep = [product['price'] for product in serialized.data]

            order_create = Order.objects.create(fullName=request.user.profile.fullName,
                                                email=request.user.profile.email,
                                                phone=request.user.profile.phone,

                                                totalCost=sum(rep),
                                                profile_id=request.user.profile.pk)

            order_create.product.add(*queryset)

            order_create.save()

            return Response({'order_id': {order_create.pk}}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        order = Order.objects.all()
        cart = Cart(request)
        serialized = OrderSerializers(order, many=True, context=cart.cart)
        return Response(serialized.data, status=status.HTTP_200_OK)


class OrderDetailsView(APIView):
    def post(self, request, pk):
        if request.user.is_authenticated and request.user.profile.user_id == request.user.pk:

            order = Order.objects.filter(pk=pk)

            if [i.profile.pk for i in order][0] == request.user.profile.pk:

                city = request.data.get('city')
                address = request.data.get('address')

                cart = Cart(request)

                order.update(city=city, address=address)

                serialized = OrderSerializers(order, many=True, context=cart.cart)

                return Response(serialized.data, status=status.HTTP_200_OK)
            return Response("it's not your order", status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, pk):
        if request.user.is_authenticated and request.user.profile.user_id == request.user.pk:
            cart = Cart(request)

            order = Order.objects.filter(pk=pk)
            if [i.profile.pk for i in order][0] == request.user.profile.pk:

                serialized = OrderSerializers(order, many=True, context=cart.cart)

                return Response(serialized.data, status=status.HTTP_200_OK)
            return Response("it's not your order", status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


