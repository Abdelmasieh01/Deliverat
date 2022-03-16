from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:item_id>/', views.detail, name='detail'),
    path('items/add/', views.add_item, name='add_item'),
    path('merchants/<int:merch_id>/', views.merch_profile, name='profile'),
]