from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

from paypal.standard.ipn.signals import valid_ipn_received
from django.shortcuts import get_object_or_404
from .models import Order, OrderProduct

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('KWARGS: ', kwargs)


# Pakoregavus vartotoją, išsaugomas ir profilis
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        print(payment_notification)
        # payment was successful
        order = get_object_or_404(Order, id=ipn.custom)
        print(order)
        order_products = OrderProduct.objects.filter(order__user=order.user, ordered=False, order__ordered=False)
        print(order_products)
        print()
        if order.total_cost() == ipn.mc_gross:
            print("The if works")
        print(type(order.total_cost()))
        print(order.total_cost())
        print(type(ipn.mc_gross))
        print(ipn.mc_gross)


        if order.total_cost() == ipn.mc_gross:
            for product in order_products:
                product.ordered = True
                print(product)
            order.ordered = True
            order_products.save()
            order.save()
            print("It worked")