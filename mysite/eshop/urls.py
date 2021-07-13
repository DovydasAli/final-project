from django.urls import path

from . import views

app_name = 'eshop'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/<slug>/', views.ProductDetailView.as_view(), name='product'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('search/', views.search, name='search'),
    path('search/<slug>/', views.ProductDetailView.as_view(), name='search-product'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
]