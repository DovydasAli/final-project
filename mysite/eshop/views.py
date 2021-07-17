from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Product, Category, SubCategory, OrderProduct, Order
from django.views import generic

from django.core.paginator import Paginator

from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

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

class OrderSummaryView(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        try:
            order = OrderProduct.objects.filter(order__user=self.request.user, ordered=False, order__ordered=False)
            total = 0
            for order_item in order:
                total += order_item.get_final_price()
            context = {
                'object': order,
                'total': format(total, ".2f")  #allows only 2 decimal after dot
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

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

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order, created = Order.objects.get_or_create(user=request.user, ordered=False)
    order_product, created = OrderProduct.objects.get_or_create(product=product, order=order)
    if order_product:
        order_product.quantity += 1
        order_product.save()
    messages.success(request, "Cart updated, product added!")
    return redirect('eshop:order-summary')

@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = OrderProduct.objects.filter(order__user=request.user, ordered=False, order__ordered=False)
    try:
        order_product = order_qs.get(product__slug=product.slug)
        order_product.quantity -= 1
        order_product.save()
        if order_product.quantity == 0:
            order_qs.filter(product__slug=product.slug).delete()
    except:
        messages.warning(request, "This product isn't in your cart!")
        return redirect('eshop:order-summary')
    messages.success(request, "Cart updated, product removed!")
    return redirect('eshop:order-summary')

@login_required
def full_remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = OrderProduct.objects.filter(order__user=request.user, ordered=False, order__ordered=False)
    try:
        order_product = order_qs.get(product__slug=product.slug)
        order_qs.filter(product__slug=product.slug).delete()
    except:
        messages.warning(request, "This product isn't in your cart!")
        return redirect('eshop:order-summary')
    messages.success(request, "Cart updated, product removed!")
    return redirect('eshop:order-summary')
