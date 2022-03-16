from django import forms
#import for labels
from django.utils.translation import gettext_lazy as _
from .models import Address, Order, Cashout

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = {'gov', 'dis', 'street', 'mark'}
        #Change default label names
        labels = {
            'gov': _('Government'),
            'dis': _('District / City'),
            'mark': _('Distinctive mark')
        }

class OrderForm(forms.ModelForm):
    qty = forms.IntegerField(min_value=1, label='Quantity', widget=forms.NumberInput) 
    class Meta:
        model = Order
        fields = ['qty']

class CashoutForm(forms.ModelForm):
    class Meta:
        model = Cashout
        fields = {'address'}
    