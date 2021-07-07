from django.contrib import admin
from .models import Product, Category, SubCategory, OrderProduct, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_id', 'category', 'sub_category', 'description', 'price')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(OrderProduct)
admin.site.register(Order)
