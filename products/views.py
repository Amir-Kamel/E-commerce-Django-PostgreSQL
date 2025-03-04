from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.views.generic.edit import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

def all_products(request):
    category_id = request.GET.get('category_id')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    return render(request, 'products/all_products.html', {'products': products})

def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'products/all_categories.html', {'categories': categories})

def product_view(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return render(request, '404.html', status=404)

    return render(request, 'products/product.html', {'product': product})


class AddCategoryView(LoginRequiredMixin ,CreateView):
    model = Category
    template_name = "forms/category_form.html"
    form_class = CategoryForm
    success_url = reverse_lazy('all_categories')
    context_object_name = "category"

class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "forms/category_form.html"
    form_class = CategoryForm
    success_url = reverse_lazy('all_categories')
    context_object_name = "category"
    pk_url_kwarg = "category_id"

class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "forms/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy('all_products')
    context_object_name = "product"

class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "forms/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy('all_products')
    context_object_name = "product"
    pk_url_kwarg = "product_id"

class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'forms/product_confirm_delete.html'
    success_url = reverse_lazy('all_products')
    context_object_name = "product"
    pk_url_kwarg = "product_id"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('all_products')

@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "cart/cart.html", {"cart_items": cart_items, "total_price": total_price})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_view")

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart_view')

