from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Product, Category, SubCategory, OrderProduct, Order
from django.views import generic

from django.core.paginator import Paginator

from django.db.models import Q

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
    paginator = Paginator(Product.objects.all(), 6)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    context = {
        'products': paged_products
    }
    return render(request, 'products.html', context=context)

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product.html'

class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 6
    template_name = 'category_list.html'

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_success_url(self):
        return reverse('category-detail', kwargs={'pk': self.object.id})

def search(request):
    query = request.GET.get('query')
    search_results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'search.html', {'products': search_results, 'query': query})

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
    else:
        order = Order.objects.create(user=request.user)
        order.products.add(order_product)
    return redirect('eshop:product', slug=slug)
