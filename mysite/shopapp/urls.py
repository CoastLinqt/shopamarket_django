from django.urls import path, include
from .views import (ProductDetailView,
                    TagsView,
                    ProductDetailReviewView,
                    OrderPostView,
                    OrderDetailsView,
                    PaymentView,
                    )

urlpatterns = [
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product"),
    path("product/<int:pk>/reviews/", ProductDetailReviewView.as_view(), name="product_review"),
    path("tags/", TagsView.as_view(), name="tags"),
    path("orders/", OrderPostView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderDetailsView.as_view(), name='orders_details'),
    path("payment/<int:pk>/", PaymentView.as_view(), name='payment')

    ]