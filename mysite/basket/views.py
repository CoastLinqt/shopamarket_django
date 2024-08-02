from django.shortcuts import render
from rest_framework.response import Response
from shopapp.models import Product
from rest_framework.views import APIView
from catalog.serializers import CatalogProductSerializers
from rest_framework import status
from django.http import HttpRequest, HttpResponse
from .service import Cart

class BasketView(APIView):

    def get(self, request):
        cart = Cart(request)


        queryset = Product.objects.all()[:1]

        serialized = CatalogProductSerializers(queryset, many=True)


        return Response( {1:{ 'count': 2}}, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        print(request.data)
        cart = Cart(request)
        product = request.data
        re = cart.add(product=product['id'], quantity=product['count'])



        return Response({"id": 123, 'count': ''}, status=status.HTTP_200_OK)



