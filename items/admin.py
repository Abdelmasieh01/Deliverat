from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'price')
    fieldsets = (
        ('Merchant:', {
            'fields': ('user',)
        }),
        ('Item Detail:', {
            'fields': ('name', 'des', 'price', 'stock')
        }),
        ('Score', {
            'fields': ('score',)
        }),
        ('Image', {
            'fields': ('img',)
        }),
    )


admin.site.register(Item, ItemAdmin)