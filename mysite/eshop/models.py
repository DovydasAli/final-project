from django.db import models
from django.urls import reverse

import uuid

from django.contrib.auth.models import User

from django.db.models import Avg

from PIL import Image

from django_countries.fields import CountryField

class Product(models.Model):
    name = models.CharField('Name', max_length=200)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)
    description = models.TextField(
        'Description', max_length=1000, help_text='Short description of the product')
    price = models.FloatField('Price', help_text='Price of the product')
    discount_price = models.FloatField(blank=True, null=True)
    picture = models.ImageField('Picture', upload_to='pictures', null=True)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name} {self.price}€"

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

    @property
    def avg_rating(self):
        rating = ProductReview.objects.filter(product=self.pk).aggregate(Avg('rating'))['rating__avg']
        if rating == None:
            return None
        rounded_rating = round(rating)
        return rounded_rating

class ProductReview(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    Rating_CHOICES = (
        (1, 'Poor'),
        (2, 'Average'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent')
    )

    rating = models.IntegerField(choices=Rating_CHOICES, default=1)
    content = models.TextField('Review', max_length=2000)

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
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

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

    def total_cost(self):
        return sum([product.get_final_price() for product in self.orderproduct_set.all()])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)

class BillingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=10)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Billing address'
        verbose_name_plural = 'Billing addresses'