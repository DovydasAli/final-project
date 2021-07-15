from django import template
from ..models import OrderProduct

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = OrderProduct.objects.filter(order__user=user, ordered=False, order__ordered=False)
        if qs:
            return qs.count()
    return 0