from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from item.models import Item, Receive, Issue

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        get_total_balance = serializers.BooleanField(source='Item.get_total_balance')
        fields = ('name', 'item_sage_id', 'sub_category', 'get_total_balance', 'unit', 'status', 'shelf_lbl')

class ReceiveSerializer(ModelSerializer):
    class Meta:
        model = Receive
        fields = ('__all__')

class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ('__all__')