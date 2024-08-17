from rest_framework.views import APIView
from .models import Product, Tag, Order, Payment
from rest_framework.response import Response
from catalog.serializers import TagsSerializers
from .serializers import (
    ProductDetailsSerializers,
    ReviewDetailsSerializers,
    OrderSerializers,
    OrderFormSerializers,
    PaymentSerializers,
)
from rest_framework import status
from basket.serializers import BasketSerializers
from basket.service import Cart
from django.db.models import Avg, Count
from bulk_update.helper import bulk_update
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema


class ProductDetailView(APIView):
    @swagger_auto_schema(responses={200: ProductDetailsSerializers})
    def get(self, request, pk):
        queryset = (
            Product.objects.filter(pk=pk)
            .select_related("category")
            .prefetch_related(
                "tags",
            )
        )
        serialized = ProductDetailsSerializers(queryset, many=True)

        return Response(serialized.data[0])


class ProductDetailReviewView(APIView):
    @swagger_auto_schema(responses={200: ReviewDetailsSerializers})
    def post(self, request, pk):
        data_dict = {}
        author = request.data["author"]
        email = request.data["email"]
        text = request.data["text"]
        rate = request.data["rate"]
        product = pk
        data_dict.update(
            author=author, email=email, text=text, rate=rate, product=product
        )

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
    @swagger_auto_schema(responses={200: OrderSerializers, 401: "need to register"})
    @transaction.atomic()
    def post(self, request):
        cart = Cart(request)
        if (
            request.user.is_authenticated
            and request.user.profile.user_id == request.user.pk
        ):
            product_id = [product for product in cart.cart.keys()]

            queryset = (
                Product.objects.filter(pk__in=product_id)
                .prefetch_related("reviews")
                .annotate(rate=Avg("reviews__rate"), product_count=Count("reviews__pk"))
            )

            serialized = BasketSerializers(queryset, many=True, context=cart.cart)

            price = [product["price"] for product in serialized.data]

            order_create = Order.objects.create(
                fullName=request.user.profile.fullName,
                email=request.user.profile.email,
                phone=request.user.profile.phone,
                totalCost=sum(price),
                profile_id=request.user.profile.pk,
            )

            order_create.product.add(*queryset)
            order_create.save()
            print({"order_id": order_create.pk})

            return Response({"order_id": order_create.pk}, status=status.HTTP_200_OK)
        return Response(
            {"messages: need to register"}, status=status.HTTP_401_UNAUTHORIZED
        )

    @swagger_auto_schema(responses={200: OrderSerializers})
    def get(self, request):
        print(request.user.profile.pk)
        order = (
            Order.objects.filter(profile_id=request.user.profile.pk)
            .select_related("profile")
            .prefetch_related("product")
        )
        serialized = OrderSerializers(order, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)


class OrderDetailsView(APIView):
    @swagger_auto_schema(
        operation_description="paymentType - Тип оплаты, может быть online или someone, "
        "deliveryType - Доставка free или express, "
        "city - Город проживания, "
        "address - Адрес проживания, ",
        request_body=OrderFormSerializers,
        responses={201: OrderSerializers},
    )
    def post(self, request, pk):
        if (
            request.user.is_authenticated
            and request.user.profile.user_id == request.user.pk
        ):
            order = Order.objects.filter(pk=pk)

            if order.exists():
                totalCost = order[0].totalCost

                if [i.profile.pk for i in order][0] == request.user.profile.pk:
                    paymentType = request.data.get("paymentType")
                    deliveryType = request.data.get("deliveryType")
                    city = request.data.get("city")
                    address = request.data.get("address")

                    cart = Cart(request)

                    if deliveryType == "express":
                        totalCost += 500

                    if deliveryType == "free" and totalCost < 2000:
                        totalCost += 200

                    order.update(
                        paymentType=paymentType,
                        deliveryType=deliveryType,
                        city=city,
                        address=address,
                        totalCost=totalCost,
                    )

                    serialized = OrderSerializers(order, many=True, context=cart.cart)

                    return Response(serialized.data, status=status.HTTP_201_CREATED)

                return Response("it's not your order", status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        responses={
            200: OrderSerializers,
            404: "it's not your order",
            401: "UNAUTHORIZED",
        }
    )
    def get(self, request, pk):
        if (
            request.user.is_authenticated
            and request.user.profile.user_id == request.user.pk
        ):
            cart = Cart(request)

            order = Order.objects.filter(pk=pk)
            if [i.profile.pk for i in order][0] == request.user.profile.pk:
                serialized = OrderSerializers(order, many=True, context=cart.cart)

                return Response(serialized.data, status=status.HTTP_200_OK)
            return Response("it's not your order", status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PaymentView(APIView):
    @swagger_auto_schema(
        request_body=PaymentSerializers,
        responses={
            400: "we don't have this count product",
            404: "it's not your order",
            401: "UNAUTHORIZED",
        },
    )
    @transaction.atomic()
    def post(self, request, pk):
        if (
            request.user.is_authenticated
            and request.user.profile.user_id == request.user.pk
        ):
            result_update = []
            cart = Cart(request)

            number = request.data.get("number")
            name = request.data.get("name")
            month = request.data.get("month")
            year = request.data.get("year")
            code = request.data.get("code")

            order = Order.objects.filter(pk=pk).prefetch_related("product")

            if [i.profile.pk for i in order][0] == request.user.profile.pk:
                payment_create = Payment.objects.create(
                    number=number,
                    name=name,
                    month=month,
                    year=year,
                    code=code,
                    order_id=[id_order.pk for id_order in order][0],
                )
                payment_create.save()
                order.update(status="success")

                for products in order:
                    for product in products.product.all():
                        product.count = product.count - cart.cart.get(
                            f"{product.pk}"
                        ).get("count")

                        if product.count < 0:
                            return Response(
                                {
                                    "message": f"we don't have this count product {product.title}"
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                        result_update.append(product)

                bulk_update(result_update)

                cart.clear()

                return Response(status=status.HTTP_200_OK)

            return Response("it's not your order", status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
