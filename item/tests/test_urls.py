from django.urls import reverse, resolve
from django.test import TestCase


class TestUrls(TestCase):
    
    def test_home_url_resolves(self):
        path = reverse('item:home')
        assert resolve(path).view_name == 'item:home'

    def test_detail_url_resolves(self):
        path = reverse('item:detail', kwargs={'slug':'ppr-pipe-20mm'})
        assert resolve(path).view_name == 'item:detail'

    def test_receive_url_resolves(self):
        path = reverse('item:receive')
        assert resolve(path).view_name == 'item:receive'
    
    def test_issue_url_resolves(self):
        path = reverse('item:issue')
        assert resolve(path).view_name == 'item:issue'

    def test_item_add_url_resolves(self):
        path = reverse('item:item-add')
        assert resolve(path).view_name == 'item:item-add'

    def test_search_url_resolves(self):
        path = reverse('item:search')
        assert resolve(path).view_name == 'item:search'



