from django.urls import path, include
from .views import BasketView
from rest_framework.routers import DefaultRouter

app_name = "basket"

urlpatterns = [
    path("basket/", BasketView.as_view(), name="basket"),
   ]