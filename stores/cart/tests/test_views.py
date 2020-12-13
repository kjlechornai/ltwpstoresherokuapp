from django.contrib.auth.models import User, AnonymousUser
from cart.views import OrderSummaryView, add_to_cart, remove_from_cart, remove_single_item_from_cart, CheckoutView, StoreIssueView
from mixer.backend.django import mixer
import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib import messages

# VIEWS IN CART APP:
    # 1.OrderSummaryView
    # 2.add_to_cart
    # 3.remove_from_cart
    # 4.remove_single_item_from_cart
    # 5.CheckoutView
    # StoreIssueView


@pytest.fixture
def item(db):
    return mixer.blend('item.Item', slug='some-slug')

@pytest.fixture
def user(db):
    return mixer.blend(User)

@pytest.fixture
def order_item(db, user, item):
    orderitem = mixer.blend('cart.OrderItem', ordered=False, user=user, item=item, quantity=5)
    return orderitem

@pytest.fixture
def order(db, user, item, order_item):
    order = mixer.blend('cart.Order', ordered=False, user=user)
    order.items.add(order_item)
    return order

# @pytest.mark.skip(reason='pass for now')
def test_order_summary_view(factory, user, order):
    path = reverse('cart:order-summary')
    request = factory.get(path)
    request.user = user

    response = OrderSummaryView.as_view()(request)
    assert response.status_code == 200


# TESTING ADD_TO_CART VIEW IS AUTHENTICATED
def test_add_to_cart_view_authenticated(factory, item, user, order, order_item):
    path = reverse('cart:add-to-cart', kwargs={'slug':'some-slug'})
    request = factory.get(path)
    request.user = user
    response = add_to_cart(request, slug=item.slug)

    assert response.status_code == 302
    # assert 'cart/order-summary' in response.url

# TESTING ADD_TO_CART VIEW IS NOT AUTHENTICATED
def test_add_to_cart_view_unauthenticated(factory, item, user, order, order_item):
    path = reverse('cart:add-to-cart', kwargs={'slug':'some-slug'})
    request = factory.get(path)
    request.user = AnonymousUser()
    
    response = add_to_cart(request, slug=item.slug)
    assert 'accounts/login' in response.url

# TESTING REMOVE_FROM_CART VIEW WITH AN ACTIVE ORDER
def test_remove_from_cart_view_with_active_order(factory, item, user, order, order_item):
    path = reverse('cart:remove-from-cart', kwargs={'slug':'some-slug'})
    request = factory.get(path)
    request.user = user 
    response = remove_from_cart(request, slug=item.slug)

    assert 'cart/order-summary' in response.url
    assert response.status_code == 302

# TESTING REMOVE_FROM_CART VIEW WITHOUT AN ACTIVE ORDER
def test_remove_from_cart_view_without_active_order(factory, item, user, order_item):
    path = reverse('cart:remove-from-cart', kwargs={'slug':'some-slug'})
    request = factory.get(path)
    request.user = user
    response = remove_from_cart(request, slug=item.slug)

    assert '/detail' in response.url
    assert response.status_code == 302

# TESTING REMOVE_SINGLE_ITEM_FROM_CART VIEW WITHOUT AN ACTIVE ORDER
def test_remove_single_item_from_cart_view(factory, item, user, order, order_item):
    path = reverse('cart:remove-single-item-from-cart', kwargs={'slug':'some-slug'})
    request = factory.get(path)
    request.user = user
    response = remove_single_item_from_cart(request, slug=item.slug)
    order_item.save()

    assert 'cart/order-summary' in response.url

def test_checkout_view(factory, user, order):
    path = reverse('cart:checkout')
    request = factory.get(path)
    request.user = user

    response = CheckoutView.as_view()(request)
    assert response.status_code == 200

def test_storeissue_view(factory, user, order):
    path = reverse('cart:order-fulfillment')
    request = factory.get(path)
    request.user = user

    response = StoreIssueView.as_view()(request)
    assert response.status_code == 200
    



