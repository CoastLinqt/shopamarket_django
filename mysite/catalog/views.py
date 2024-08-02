from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Categories
from shopapp.models import Product, Sales, Review
from rest_framework import pagination
from rest_framework.viewsets import ModelViewSet
from .serializers import CatalogProductSerializers, SalesSerializer, CategorySerializer
from django.db.models import Avg, Count, Prefetch


class CategoriesView(APIView):
    def get(self, request: Request):
        categories = Categories.objects.filter(parent=None)
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_paginated_response(self, data):

        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
            },
            status=status.HTTP_200_OK,
        )


class CategoriesViewSET(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = CatalogProductSerializers
    pagination_class = CustomPagination


class CatalogView(APIView):

    def filter_queryset(self, products):

        name = self.request.GET.get("filter[name]", "").strip()
        minPrice = float(self.request.GET.get("filter[minPrice]", ""))
        maxPrice = float(self.request.GET.get("filter[maxPrice]", ""))
        freeDelivery = self.request.GET.get("filter[freeDelivery]", "").capitalize()
        available = self.request.GET.get("filter[available]", "").capitalize()
        sort = self.request.GET.get("sort", "")
        sortType = self.request.GET.get("sortType", "")

        prefetch = Prefetch('reviews', Review.objects.all())

        try:
            category = int(self.request.META.get("HTTP_REFERER", "").split("/")[4])
            if category:
                products = products.filter(category__pk=category)
        except ValueError:
            products = products.filter(category__pk=1)

        products = products.filter(price__range=(minPrice, maxPrice))

        if name:
            products = products.filter(title__icontains=name)

        if freeDelivery:
            products = products.filter(freeDelivery=freeDelivery)

        if available:
            products = products.filter(active=available)

        if sort == "price" or sort == "date":
            if sortType == "dec":

                products = products.order_by(f"-{sort}")

            if sortType == "inc":
                products = products.order_by(str(sort))

        if sort == "rating":
            if sortType == "dec":
                products = products.prefetch_related(prefetch).annotate(
                    rate=Avg('reviews__rate')).order_by('-rate')

            if sortType == "inc":
                products = products.prefetch_related(prefetch).annotate(
                    rate=Avg('reviews__rate')).order_by('rate')

        if sort == "reviews":

            if sortType == "dec":
                products = products.prefetch_related(prefetch).annotate(
                    product=Count('reviews__pk')).order_by('-product')

            if sortType == "inc":
                products = products.prefetch_related(prefetch).annotate(
                    product=Count('reviews__pk')).order_by('product')

        return products

    def get(self, request):

        queryset = Product.objects.all()

        paginator = CustomPagination()

        products = self.filter_queryset(products=queryset)

        paginated_products = paginator.paginate_queryset(products, request)

        serialized = CatalogProductSerializers(paginated_products, many=True)

        return paginator.get_paginated_response(serialized.data)


class CatalogPopularView(APIView):

    def get(self, request):
        prefetch = Prefetch('reviews', Review.objects.all())
        products = Product.objects.all().prefetch_related(prefetch).annotate(
            rate=Avg('reviews__rate')).order_by('-rate')

        serialized = CatalogProductSerializers(products, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)


class CatalogLimitedView(APIView):

    def get(self, request):
        queryset = Product.objects.filter(limited=True)[:5]
        serialized = CatalogProductSerializers(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class CatalogSalesView(APIView):
    def get(self, request):
        sales = Sales.objects.all()

        paginator = CustomPagination()

        paginated = paginator.paginate_queryset(sales, request)

        serialized = SalesSerializer(paginated, many=True)

        return paginator.get_paginated_response(serialized.data)


class BannersView(APIView):
    def get(self, request):
        prefetch = Prefetch('reviews', Review.objects.all())
        products = Product.objects.all().prefetch_related(prefetch).annotate(
            product=Count('reviews__pk')).order_by('-product')[:3]

        serialized = CatalogProductSerializers(products, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)
