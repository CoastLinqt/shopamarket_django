from django.urls import path, include
from .views import ProductDetailView, TagsView, ProductDetailReviewView




urlpatterns = [
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product"),
    path("product/<int:pk>/reviews/", ProductDetailReviewView.as_view(), name="product_review"),
    path("tags/", TagsView.as_view(), name="tags"),

    ]