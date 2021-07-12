from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>', views.product, name='product'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('search/', views.search, name='search'),
    path('search/<int:product_id>', views.product, name='search-product'),
]