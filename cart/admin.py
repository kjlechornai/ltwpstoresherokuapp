from django.contrib import admin
from . models import OrderItem, Order, OrderPurpose, OrderIssued

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(OrderPurpose)
admin.site.register(OrderIssued)
