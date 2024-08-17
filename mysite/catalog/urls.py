from django.urls import path, include
from .views import (
    CategoriesView,
    CatalogView,
    CategoriesViewSET,
    CatalogPopularView,
    CatalogLimitedView,
    CatalogSalesView,
    BannersView,
)
from rest_framework.routers import DefaultRouter

app_name = "catalog"

routers = DefaultRouter()

routers.register("catalog", CategoriesViewSET)

urlpatterns = [
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("products/popular/", CatalogPopularView.as_view(), name="catalog_popular"),
    path("products/limited/", CatalogLimitedView.as_view(), name="catalog_limited"),
    path("sales/", CatalogSalesView.as_view(), name="sales"),
    path("banners/", BannersView.as_view(), name="banners"),
    path("api/", include(routers.urls)),
]
