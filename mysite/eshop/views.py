from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from .models import Product, Category, SubCategory, OrderProduct, Order

def index(request):
    num_products = Product.objects.all().count()
    num_categories = Category.objects.all().count()
    num_sub_categories = SubCategory.objects.all().count()

    num_orders = Order.objects.count()

    context = {
        'num_products': num_products,
        'num_categories': num_categories,
        'num_sub_categories': num_sub_categories,
        'num_orders': num_orders,
    }

    return render(request, 'index.html', context=context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    print(products)
    return render(request, 'products.html', context=context)

def product(request, product_id):
    single_product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': single_product})
