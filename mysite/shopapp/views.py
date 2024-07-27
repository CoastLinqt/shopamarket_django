from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from .models import Product
from .serializers import ProductSerializer


class ProductsListView(ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

