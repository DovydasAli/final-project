from django.db import models
from django.urls import reverse

import uuid

from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField('Name', max_length=200)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)
    description = models.TextField('Description', max_length=1000, help_text='Short description of the product')
    price = models.FloatField('Price', help_text='Price of the product')
    discount_price = models.FloatField(blank=True, null=True)
    picture = models.ImageField('Picture', upload_to='pictures', null=True)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.slug} {self.name}: {self.category} {self.description} {self.price}€"

    def get_absolute_url(self):
        return reverse('eshop:product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('eshop:add-to-cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('eshop:remove-from-cart', kwargs={
            'slug': self.slug
        })

class Category(models.Model):
    name = models.CharField('Name', max_length=200)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    name = models.CharField('Name', max_length=200)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Sub category'
        verbose_name_plural = 'Sub categories'

class OrderProduct(models.Model):
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_total_savings(self):
        return round(self.get_total_product_price() - self.get_total_discount_product_price(), 2)

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_product_price()
        else:
            return self.get_total_product_price()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    STATUS = (
        ('order placed', 'Order placed'),
        ('in progress', 'In progress'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS,
        blank=True,
        default='order placed',
        help_text='Status',
    )

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.user} {self.date_created}"
