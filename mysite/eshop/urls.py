from django.urls import path

from . import views

app_name = 'eshop'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/<slug>/', views.ProductDetailView.as_view(), name='product'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('subcategory/<int:pk>', views.SubCategoryDetailView.as_view(), name='subcategory-detail'),
    path('search/', views.search, name='search'),
    path('search/<slug>/', views.ProductDetailView.as_view(), name='search-product'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('full-remove-from-cart/<slug>/', views.full_remove_from_cart, name='full-remove-from-cart'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),
]