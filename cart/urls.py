from django.urls import path
from .views import OrderSummaryView, add_to_cart, remove_from_cart, remove_single_item_from_cart, CheckoutView, StoreIssueView

app_name = 'cart'
urlpatterns = [
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-fulfillment/', StoreIssueView.as_view(), name='order-fulfillment'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
]