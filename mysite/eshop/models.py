from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField('Name', max_length=200)
    unique_id = models.CharField('Unique id', max_length=20, help_text='Randomly generated product id code')  # bandyti padaryt unikalu id jei neiseis istrynt
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)
    description = models.TextField('Description', max_length=1000, help_text='Short description of the product')
    price = models.FloatField('Price', help_text='Price of the product')

    def __str__(self):
        return f"{self.unique_id} {self.name}: {self.category} {self.description} {self.price}"

class Category(models.Model):
    name = models.CharField('Name', max_length=200)

    def __str__(self):
        return f"{self.name}"

class SubCategory(models.Model):
    name = models.CharField('Name', max_length=200)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"

class OrderProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product}"

class Order(models.Model):
    products = models.ManyToManyField('OrderProduct')
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.products} {self.date_created}"