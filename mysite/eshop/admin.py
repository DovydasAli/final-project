from django.contrib import admin
from .models import Product, Category, SubCategory, OrderProduct, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_id', 'category', 'sub_category', 'description', 'price')
    list_filter = ('category', 'sub_category')
    fieldsets = (
        (None, {
            'fields': ('name', 'unique_id')
        }),
        ('Categorisation', {
            'fields': ('category', 'sub_category')
        }),
        ('Product information', {
            'fields': ('description', 'price')
        }),
    )
    search_fields = ('name', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    list_filter = ('category', )

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'date_created')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(OrderProduct)
admin.site.register(Order)
