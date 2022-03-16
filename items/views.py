from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets, permissions
from .serializers import ItemSerializer
from .models import Item
from .forms import ItemForm
from request.models import Order
from request.forms import OrderForm

def index(request):
    """ Ordering the items list by score (how many times they are bought)
        then by the price """
    items = Item.objects.all().order_by('-score', '-price')
    return render(request, 'base.html', {'items': items, 'home': True, 'success': False, 'merchant': None})

def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            user = request.user
            try:
                """Checking if the user has ordered this item before, so the quantity
                is added instead of having them as many different orders"""
                order = Order.objects.get(user=user, item=item)
                prev_quantity = order.quantity
                order.quantity += form.cleaned_data.get('qty')
                #Difference in quantity to add to item score
                diff_quantity = order.quantity - prev_quantity
                #Force order to not ordering more than item stock
                if diff_quantity > item.stock:
                    order.quantity -= (diff_quantity - item.stock)
                    order.save()
                    diff_quantity = item.stock
                #Get difference of orders
                item.score += diff_quantity
                item.stock -= diff_quantity
                item.save()
                order.save()
                return redirect('request:my_orders')
            except Order.DoesNotExist:
                quantity = form.cleaned_data.get('qty')
                order = Order(user=user, item=item, quantity=quantity)
                #Force order to not ordering more than item stock
                if order.quantity > item.stock:
                    order.quantity = item.stock
                    order.save()
                item.score += order.quantity
                item.stock -= order.quantity
                item.save()
                order.save()
                return redirect('request:my_orders')
    form = OrderForm()
    return render(request, 'items/detail.html', {'item': item, 'form':form})

#To add an item to the market, you must be logged in
@login_required(login_url='/login/')
def add_item(request):
    #Checking if the logged in user is of group 'Merchant', meaning he can sell stuff
    if request.user.groups.filter(name='Merchant').exists():
        if request.method == 'POST':
            #Get the request post and files
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                user = request.user
                name = form.cleaned_data.get('name')
                des = form.cleaned_data.get('des')
                price = form.cleaned_data.get('price')
                #Gettng the image from the request
                img = request.FILES['img']
                stock = form.cleaned_data.get('stock')
                item = Item(user=user, name=name, des=des, price=price, img=img, stock=stock)
                item.save()
                return redirect('items:index')
            else:
                #If form is not valid, set not_valid to True to show message in HTML
                return render(request, 'items/add_item.html', {'form': form, 'not_valid': True})
        form = ItemForm()
        return render(request, 'items/add_item.html', {'form': form, 'not_valid': False})
    else:
        #Redirect the user to the index page if not of group 'Merchant'
        return redirect('items:index')

def merch_profile(request, merch_id):
    merchant = User.objects.get(id=merch_id)
    items = Item.objects.filter(user=merchant)
    return render(request, 'base.html', {'items': items, 'home': False, 'success': False, 'merchant': merchant})

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-score', '-price')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]