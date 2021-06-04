from django import template
from ShopCore.models import Order

register = template.Library()

@register.filter
def productCount(user):
    if user.is_authenticated:
        order = Order.objects.filter(user=user, ordered=False)
        if order.exists():
            return order[0].products.count()
    return 0