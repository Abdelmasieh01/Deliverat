from django.urls import path
from . import views

app_name = 'request'

urlpatterns= [
    path('add/address/', views.add_address, name='add_address'),
    path('me/addresses/', views.my_addresses, name='my_addresses'),
    path('me/orders/', views.my_orders, name='my_orders'),
    path('me/orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('me/addresses/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    path('me/addresses/<int:address_id>/edit/', views.edit_address, name='edit_address'),
    path('me/notifications/', views.my_notifications, name='my_nots')
]