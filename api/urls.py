from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

api_router = DefaultRouter()

api_router.register("users", UsersViewSet, basename="users")
api_router.register("products", ProductViewSet, basename="products")
api_router.register("cart", CartItemViewSet, basename="cart")

urlpatterns = [
    path("", include(api_router.urls))
]