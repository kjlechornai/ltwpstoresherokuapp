from django.urls import reverse, resolve
from django.test import TestCase


class TestUrls(TestCase):
    
    def test_order_summary_url_resolves(self):
        path = reverse('cart:order-summary')
        assert resolve(path).view_name == 'cart:order-summary'

    def test_add_to_cart_url_resolves(self):
        path = reverse('cart:add-to-cart', kwargs={'slug':'ppr-pipe-20mm'})
        assert resolve(path).view_name == 'cart:add-to-cart'

    def test_remove_from_cart_url_resolves(self):
        path = reverse('cart:remove-from-cart', kwargs={'slug':'ppr-pipe-20mm'})
        assert resolve(path).view_name == 'cart:remove-from-cart'
    
    def test_checkout_url_resolves(self):
        path = reverse('cart:checkout')
        assert resolve(path).view_name == 'cart:checkout'

    def test_cart_remove_single_item_url_resolves(self):
        path = reverse('cart:remove-single-item-from-cart', kwargs={'slug':'ppr-pipe-20mm'})
        assert resolve(path).view_name == 'cart:remove-single-item-from-cart'

    def test_order_fulfillment_url_resolves(self):
        path = reverse('cart:order-fulfillment')
        assert resolve(path).view_name == 'cart:order-fulfillment'