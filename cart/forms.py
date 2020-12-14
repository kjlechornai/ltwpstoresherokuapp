from django.forms import ModelForm
from .models import OrderPurpose, OrderIssued


class CheckoutForm(ModelForm):
    class Meta:
        model = OrderPurpose
        fields = ['purpose', 'project_name', 'department', 'collected_by']

class OrderIssueForm(ModelForm):
    class Meta:
        model = OrderIssued
        fields = ['issuer', 'location']