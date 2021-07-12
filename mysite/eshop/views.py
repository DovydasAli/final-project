from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, reverse
from .models import Product, Category, SubCategory, OrderProduct, Order
from django.views import generic

from django.core.paginator import Paginator

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

def product(request, product_id):
    single_product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': single_product})

class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 6
    template_name = 'category_list.html'

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_success_url(self):
        return reverse('category-detail', kwargs={'pk': self.object.id})
