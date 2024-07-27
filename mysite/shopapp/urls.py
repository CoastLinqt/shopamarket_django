from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductsListView

urlpatterns = [
    path("catalog/", ProductsListView.as_view(), name="catalog"),
    ]