from django.contrib import admin
from .models import Product, Category, OrderProduct, Order

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderProduct)
admin.site.register(Order)
