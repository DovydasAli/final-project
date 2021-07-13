from django.db import models
from django.urls import reverse
import uuid

class Product(models.Model):
    name = models.CharField('Name', max_length=200)
    unique_id = models.CharField('Unique id', max_length=100, blank=True, unique=True, default=uuid.uuid4)  # bandyti padaryt unikalu id jei neiseis istrynt
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)
    description = models.TextField('Description', max_length=1000, help_text='Short description of the product')
    price = models.FloatField('Price', help_text='Price of the product')
    discount_price = models.FloatField(blank=True, null=True)
    picture = models.ImageField('Picture', upload_to='pictures', null=True)

    def __str__(self):
        return f"{self.unique_id} {self.name}: {self.category} {self.description} {self.price}€"

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
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.product

class Order(models.Model):
    products = models.ManyToManyField('OrderProduct')
    date_created = models.DateTimeField(auto_now_add=True)

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
        return f"{self.products} {self.date_created}"