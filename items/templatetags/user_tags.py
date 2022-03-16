from django import template

register = template.Library()

@register.filter()
def is_merchant(user):
    #Checks if the user is a merchant
    return user.groups.filter(name='Merchant').exists()