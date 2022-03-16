from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class NewUserForm(UserCreationForm):
    
    choices = [('Yes', 'Yes'), ('No', 'No')]
    merchant = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, label='Are you a Merchant/Seller?')
    #Adding the email field, UserCreationForm doesn't have it
    email = forms.EmailField(required=True)
    
    #Defining meta class containing User model and fields in the form
    class Meta:
        model = User
        fields=('first_name', 'last_name', 'username','email', 'password1', 'password2', 'merchant')
    
    #Changing original save method to save email
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user