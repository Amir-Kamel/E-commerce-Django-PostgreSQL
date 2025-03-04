from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',all_products, name='all_products'),
    path('products/', all_products, name='all_products'),
    path('products/categories/', all_categories, name='all_categories'),
    path('products/product/<int:product_id>/', product_view, name='product_view'),

    path('categories/add_category/', AddCategoryView.as_view(), name='add_category'),
    path('categories/update_category/<int:category_id>/', UpdateCategoryView.as_view(), name='update_category'),

    path('products/add_product/', AddProductView.as_view(), name='add_product'),
    path('products/update_product/<int:product_id>/', UpdateProductView.as_view(), name='update_product'),
    path('products/delete_product/<int:product_id>/', ProductDeleteView.as_view(), name='delete_product'),

    path("cart/", cart_view, name="cart_view"),
    path("add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

