from django.urls import reverse
from django.db.models import Q
from mixer.backend.django import mixer
from item.views import (HomeView, ItemDetailView, ReceiveView, IssueView, ItemCreateView, \
    search, plumbing, technical, hse, electrical, stationery)
from item.forms import ReceiveModelForm, IssueModelForm
from item.models import Receive, Issue, Item
from django.test import RequestFactory
import pytest


def test_home_view(db, factory):
    path = reverse('item:home')
    request = factory.get(path)
    response = HomeView.as_view()(request)
    assert response.status_code == 200
    assert 'home.html' in response.template_name

def test_item_detail_view(item1, factory):
    path = reverse('item:detail', kwargs={'slug':'item-one'})
    request = factory.get(path)
    response = ItemDetailView.as_view()(request, slug=item1.slug)
    assert response.status_code == 200
    assert response.template_name == ['detail.html']
    

def test_item_receive_view_get(db, factory):
    path = reverse('item:receive')
    request = factory.get(path)
    response = ReceiveView.as_view()(request)
    assert response.status_code == 200

def test_item_receive_view_post(db, factory, item1, project1):
    data = {
        'item': item1,
        'project':project1,
        'quantity':10,
        'delivery_mode': 'road',
        'received_by': 'kizito'
        }            
    path = reverse('item:receive')
    request = factory.post(path, data=data)
    response = ReceiveView.as_view()(request)
    form = ReceiveModelForm(data=data)
    if form.is_valid():
        receive = form.save()
        assert receive.item == item1
    assert response.status_code == 302
    assert response.url == '/receive/'
    
def test_item_issue_view_post(db, factory, item1, project1):
    data = {
        'item': item1,
        'project':project1,
        'quantity':10,
        'purpose': 'road',
        'issued_to': 'kizito',
        'issue_type': 'direct'
        }            
    path = reverse('item:issue')
    request = factory.post(path, data=data)
    response = IssueView.as_view()(request)
    form = IssueModelForm(data=data)
    if form.is_valid():
        issue = form.save()
        assert issue.item == item1
    assert response.status_code == 302
    assert response.url == '/issue/'

def test_search_view(db, factory):
    qs = Item.objects.all()
    title_contains = 'item'
    if title_contains != ' ' and title_contains is not None: 
        qs = qs.filter(Q(name__icontains=title_contains) | Q(item_sage_id__icontains=title_contains))
        print(qs)
    
    path = reverse('item:search')
    url = '{url}?{filter}={value}'.format(
        url=path,filter='title-contain', value='item')
    request = factory.get(url)
    response = search(request)
    assert response.status_code == 200
    print(response)
    

def test_plumbing_view(db, factory):
    path = reverse('item:plumbing')
    request = factory.get(path)
    response = search(request)
    assert response.status_code == 200

def test_electrical_view(db, factory):
    path = reverse('item:electrical')
    request = factory.get(path)
    response = search(request)
    assert response.status_code == 200

def test_technical_view(db, factory):
    path = reverse('item:technical')
    request = factory.get(path)
    response = search(request)
    assert response.status_code == 200

def test_hse_view(db, factory):
    path = reverse('item:hse')
    request = factory.get(path)
    response = search(request)
    assert response.status_code == 200

def test_stationery_view(db, factory):
    path = reverse('item:stationery')
    request = factory.get(path)
    response = search(request)
    assert response.status_code == 200




