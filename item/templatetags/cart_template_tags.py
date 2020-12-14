from django import template
from cart.models import Order
from item.models import Item
from django.db.models import Sum

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.filter
def project_balance(item, project):
    # qs = Item.objects.get(name=item)
    # if qs.exists():
    #     return qs.project_balance(item, project)
    # return 0
    pass