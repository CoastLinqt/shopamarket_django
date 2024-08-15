from rest_framework.response import Response
from shopapp.models import Product
from rest_framework.views import APIView
from rest_framework import status
from .service import Cart
from rest_framework.generics import get_object_or_404
from django.db.models import Avg, Count
from .serializers import BasketSerializers, BasketFormSerializers
from drf_yasg.utils import swagger_auto_schema


def get_product(session_cart):

    product_id = [product for product in session_cart.cart.keys()]

    queryset = (
        Product.objects.filter(pk__in=product_id)
        .prefetch_related("reviews")
        .annotate(rate=Avg("reviews__rate"), product_count=Count("reviews__pk"))
    )

    serialized = BasketSerializers(queryset, many=True, context=session_cart.cart)
    return serialized


class BasketView(APIView):
    @swagger_auto_schema(responses={200: BasketSerializers})
    def get(self, request):



        cart = Cart(request)


        serialized = get_product(session_cart=cart)



        return Response(
            serialized.data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=BasketFormSerializers,
                         responses={
                                200: BasketSerializers,
                                404: 'NOT FOUND'}
                         )
    def post(self, request, **kwargs):


        cart = Cart(request)

        product = request.data

        check_product = get_object_or_404(Product, pk=product.get("id"))

        if check_product:

            cart.add(
                product=check_product,
                count=int(product.get("count")),
            )

            if "False" in [key for key in cart.cart.keys()]:

                return Response(
                    {
                        "message",
                        f"The number of selected items exceeds the total quantity of goods."
                        f"Product: {check_product.title}, "
                        f"Total: {check_product.count} in shop"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:

                serialized = get_product(session_cart=cart)
                print(serialized.data)


                return Response(serialized.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=BasketFormSerializers, responses={
                                200: BasketSerializers,
                                404: 'NOT FOUND'})
    def delete(self, request):

        cart = Cart(request)
        product = request.data

        check_product = get_object_or_404(Product, pk=product.get("id"))

        if check_product:
            cart.remove(product=check_product, count=product.get("count"))

            serialized = get_product(session_cart=cart)
            return Response(serialized.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
