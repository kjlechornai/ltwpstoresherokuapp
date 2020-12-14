from django.test import TestCase, Client
from django.urls import reverse
from item.forms import ReceiveModelForm, IssueModelForm, ItemModelForm
from item.models import Issue, Receive
from datetime import datetime
from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestForms(TestCase):

    def setUp(self):
        self.client = Client()
        self.receive_path = reverse('item:receive')
        self.issue_path = reverse('item:issue')
        self.create_path = reverse('item:item-add')
        self.item = mixer.blend('item.Item')
        
       

        
    def test_receive_form_displayed(self):
        response = self.client.get(self.receive_path)
        assert response.status_code == 200

    def test_issue_form_displayed(self):
        response = self.client.get(self.issue_path)
        assert response.status_code == 200

    def test_create_item_form_displayed(self):
        response = self.client.get(self.create_path)
        assert response.status_code == 200


    def test_receive_form_is_valid(self):
        form = ReceiveModelForm(data={
            'item':self.item,
            'quantity':10,
            'status':'in good condition',
            'delivery_mode':'flight',
            'receive_date' : '2020-11-30',
            'receive_by':'kizito',
            'requestor':'brian'
        })
        assert form.is_valid() == True

    def test_receive_form_no_data(self):
        form = ReceiveModelForm(data={})
        assert form.is_valid() == False
        assert len(form.errors) == 7

    def test_issue_form_is_valid(self):
        form = IssueModelForm(data={
            'item':self.item,
            'quantity':10,
            'issued_to':'kizito',
            'issue_type':'online'
        })
        assert form.is_valid() == True

    def test_issue_form_no_data(self):
        form = IssueModelForm(data={})
        assert form.is_valid() == False
        assert len(form.errors) == 4

    def test_create_item_form_displayed(self):
        response = self.client.get(self.create_path)
        assert response.status_code == 200

    