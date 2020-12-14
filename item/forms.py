from django.forms import ModelForm, ValidationError
from .models import Receive, Issue, Item

class ReceiveModelForm(ModelForm):

    class Meta:
        model = Receive
        fields = '__all__'

class IssueModelForm(ModelForm):
    
    class Meta:
        model = Issue
        fields = '__all__'

class ItemModelForm(ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'category', 'description', 'unit', 'sub_category', 'item_sage_id', 'shelf_lbl']
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Item.objects.filter(name=name).exists():
            raise ValidationError('The item is already in the database')
        return name