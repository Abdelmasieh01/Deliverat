from django.contrib import admin
from .models import Gov, Address, Order, Cashout, Notification


# Register your models here.
admin.site.register(Gov)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user',)
    fieldsets = (
        ('Address for user: ', {
            'fields': ('user',)
        }),
        ('Address: ', {
            'fields': ('gov', 'dis', 'street', 'mark',)
        }),
    )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'user')
    fieldsets = (
        ('Order for user: ', {
            'fields': ('user',)
        }),
        ('Item: ', {
            'fields': ('item', 'quantity',)
        }),
    )

class CashoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    fieldsets = (
        ('User:', {
            'fields': ('user', 'address',)
        }),
        ('Orders:', {
            'fields': ('orders',)
        }),
    )
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cashout, CashoutAdmin)
admin.site.register(Notification)