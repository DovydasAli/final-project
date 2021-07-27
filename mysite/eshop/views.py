from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Product, Category, SubCategory, OrderProduct, Order, ProductReview, BillingAddress
from django.views import generic

from django.core.paginator import Paginator

from django.db.models import Q, Avg

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

from django.template.defaulttags import register
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect

from .forms import ProductReviewForm, UserUpdateForm, ProfileUpdateForm, CheckoutForm
from django.views.generic.edit import FormMixin

from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt


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
            billing_address = BillingAddress.objects.filter(user=self.request.user)
            for order_item in order:
                total += order_item.get_final_price()
            context = {
                'billing_address': billing_address,
                'object': order,
                'total': round(total, 2)  #allows only 2 decimal after dot
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

class CheckoutView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                zip = form.cleaned_data.get('zip')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                    city=city
                )
                try:
                    billing_address.save()
                except:
                    messages.warning(self.request, "Order already placed")
                    return redirect('eshop:checkout')
                order.billing_address = billing_address
                order.save()
                return redirect('eshop:process-payment')
            messages.warning(self.request, "Failed checkout")
            return redirect('eshop:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("eshop:order-summary")

class PaymentView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(self.request, "payment.html")

class ProductDetailView(FormMixin, generic.DetailView):
    model = Product
    template_name = 'product.html'
    form_class = ProductReviewForm

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user.is_authenticated:
            user_review = ProductReview.objects.filter(reviewer=request.user, product=product)
            context = {
                 'product': product,
                 'user_review': user_review,
                 'form': ProductReviewForm
              }
        else:
            context = {
                'product': product,
                'form': ProductReviewForm
            }
        return render(self.request, 'product.html', context)

    def get_success_url(self):
        return reverse('eshop:product', kwargs={'slug': self.object.slug})

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = ProductReviewForm(initial={'product': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.product = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(ProductDetailView, self).form_valid(form)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 6
    template_name = 'category_list.html'

    def get(self, request, *args, **kwargs):
        lowest_prices = {}
        category_list = Category.objects.all()
        for category in category_list:
            products = Product.objects.filter(category__name=category.name)
            low_prices = 0
            for product in products:  # solution for category lowest price
                if product.discount_price:
                    if low_prices == 0:
                        low_prices = product.discount_price
                    elif low_prices > product.discount_price:
                        low_prices = product.discount_price
                else:
                    if low_prices == 0:
                        low_prices = product.price
                    elif low_prices > product.price:
                        low_prices = product.price
            lowest_prices[category.name] = low_prices
        context = {
            'lowest_prices': lowest_prices,
            'category_list': category_list,
            'get_item': get_item
        }
        return render(self.request, 'category_list.html', context)

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        category_products = Product.objects.filter(category__name=category.name)
        context = {
            'object': category,
            'products': category_products
        }
        return render(self.request, 'category_detail.html', context)

    def get_success_url(self):
        return reverse('category-detail', kwargs={'pk': self.object.id})

class SubCategoryDetailView(generic.DetailView):
    model = SubCategory
    template_name = 'subcategory_detail.html'

    def get(self, request, *args, **kwargs):
        subcategory = self.get_object()
        subcategory_products = Product.objects.filter(sub_category__name=subcategory.name)
        context = {
            'object': subcategory,
            'products': subcategory_products
        }
        return render(self.request, 'subcategory_detail.html', context)

def search(request):
    query = request.GET.get('query')
    search_results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'search.html', {'products': search_results, 'query': query})

@login_required
def process_payment(request):
    user_order = Order.objects.get(user=request.user, ordered=False)
    billing_address = BillingAddress.objects.get(user=request.user)
    order = get_object_or_404(Order, id=user_order.id)
    order_products = OrderProduct.objects.filter(order__user=request.user, ordered=False, order__ordered=False)
    host = request.get_host()


    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.total_cost(),
        'invoice': 'This is invoice 64',
        'custom': str(order.id),
        'item_name': "Order {}".format(order.id),
        'address_override': 1,
        'currency_code': 'EUR',
        'address1': str(billing_address.street_address),
        'address2': str(billing_address.apartment_address),
        'country': str(billing_address.country),
        'zip': billing_address.zip,
        'city': str(billing_address.city),
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('eshop:payment-done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('eshop:payment-cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'order': order, 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('eshop:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order, created = Order.objects.get_or_create(user=request.user, ordered=False)
    order_product, created = OrderProduct.objects.get_or_create(product=product, order=order)
    if order_product:
        order_product.quantity += 1
        order_product.save()
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
        return redirect('eshop:order-summary')
    return redirect('eshop:order-summary')

@login_required
def full_remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = OrderProduct.objects.filter(order__user=request.user, ordered=False, order__ordered=False)
    try:
        order_qs.filter(product__slug=product.slug).delete()
    except:
        return redirect('eshop:order-summary')
    return redirect('eshop:order-summary')

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is taken!')
                return redirect('eshop:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with {email} is already registered!')
                    return redirect('eshop:register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('eshop:register')
    return render(request, 'register.html')
