from django import forms
from .models import Item
from django.utils.translation import gettext_lazy as _

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = {'name', 'des', 'price', 'img', 'stock'}
        #Changing field labels
        labels = {
            'name': _('Item name'),
            'des': _('Item describtion'),
            'price': _('Item price'),
            'img': _('Upload image for this item'),
            'stock': _('How many of this item you have in stock?')
        }
        #Making the describtion of Textarea instance and 3 rows long
        widgets = {
            'des': forms.Textarea(attrs={'rows': 3}),
        }