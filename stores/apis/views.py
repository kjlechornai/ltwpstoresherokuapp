from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import ItemSerializer, ReceiveSerializer, IssueSerializer
from item.models import Item, Receive, Issue

# Create your views here.
class ItemAPIView(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        contains = self.request.query_params.get('name', None)
        if contains is not None:
            queryset = Item.objects.filter(name__icontains=contains)
        return queryset   

class ReceiveAPIView(ListAPIView):
    queryset = Receive.objects.all()
    serializer_class = ReceiveSerializer

class IssueAPIView(ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class NewReceiveAPIView(CreateAPIView):
    serializer_class = ReceiveSerializer

class NewIssueAPIView(CreateAPIView):
    serializer_class = IssueSerializer




