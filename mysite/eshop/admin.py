from django.contrib import admin
from .models import Product, Category, SubCategory, OrderProduct, Order, ProductReview, Profile
from django.utils.html import mark_safe

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'sub_category', 'description', 'price', 'discount_price', 'picture')
    list_filter = ('category', 'sub_category')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        ('Categorisation', {
            'fields': ('category', 'sub_category')
        }),
        ('Product information', {
            'fields': ('description', 'price', 'discount_price')
        }),
        ('Picture', {
            'fields': ('picture', )
        }),
    )
    search_fields = ('name', )

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'date_created', 'reviewer', 'content', 'rating')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    list_filter = ('category', )

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'quantity', 'order')

    def get_name(self, obj):
        return obj.product.name
    get_name.admin_order_field = 'product'
    get_name.short_description = 'Product Name'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_created', 'status')

admin.site.register(Profile)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Order, OrderAdmin)
