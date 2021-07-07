from django.contrib import admin
from .models import Product, Category, SubCategory, OrderProduct, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_id', 'category', 'sub_category', 'description', 'price')

class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name'

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

class OrderProductAdmin(admin.ModelAdmin):
    list_display = 'product'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'date_created')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(OrderProduct)
admin.site.register(Order)
