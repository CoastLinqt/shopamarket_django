from rest_framework.views import APIView
from .models import Product, Tag, Review
from rest_framework.response import Response
from catalog.serializers import TagsSerializers
from .serializers import ProductDetailsSerializers, ReviewDetailsSerializers
from rest_framework import status


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