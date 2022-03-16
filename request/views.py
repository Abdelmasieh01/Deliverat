from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AddressForm, CashoutForm
from .models import Address, Order, Cashout, Notification
from items.models import Item

#User must be logged in to add an addresss to their account
@login_required(login_url=('/login/'))
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            user = request.user
            gov = form.cleaned_data.get('gov')
            dis = form.cleaned_data.get('dis')
            street = form.cleaned_data.get('street')
            mark = form.cleaned_data.get('mark')
            address = Address(user=user, gov=gov, dis=dis, street=street, mark=mark)
            address.save()
            return redirect('request:my_addresses')
        else:
            return render(request, 'request/add_address.html', {'form': form, 'not_valid': True})
    form = AddressForm()
    return render(request, 'request/add_address.html', {'form': form, 'not_valid': False})

@login_required(login_url=('/login/'))
def my_addresses(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    return render(request, 'request/my_addresses.html', {'addresses': addresses})

@login_required(login_url=('/login/'))
def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    if request.method == 'POST':
        form = CashoutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get('address')
            cashout = Cashout(user=user, address=address)
            cashout.save()
            cashout.orders.set(orders)
            cashout.save()
            
            for order in orders:
                #order.item.user is the merchant
                #order.user is the buyer
                Notification.objects.create(user=order.item.user, 
                buyer=order.user, order=order, address=cashout.address)

            test = User.objects.get(username='testato')
            orders.update(user=test)
            items = Item.objects.all().order_by('-score', '-price')
            context = {'items': items, 'home': True, 'success': True, 'merchant': None}
            return render(request, 'base.html', context)
        else:
            return render(request, 'request/my_orders.html', {'form': form, 'not_valid':True})
    form = CashoutForm()
    form.fields['address'].queryset = Address.objects.filter(user=user)
    user = request.user
    total = 0
    #Calculate total price for the whole cart
    for order in orders:
        total += order.tot_price()
    return render(request, 'request/my_orders.html', {'orders': orders, 'total': total, 'not_valid': False, 'form': form})

@login_required(login_url=('/login/'))
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user == order.user:
        item = Item.objects.get(id=order.item.id)
        item.score -= order.quantity
        item.stock += order.quantity
        item.save()
        order.delete()
        return redirect('request:my_orders')
    else:
        return redirect('request:my_orders')

@login_required(login_url=('/login/'))
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.user == address.user:
        address.delete()
        return redirect('request:my_addresses')
    else:
        return redirect('request:my_addresses')

@login_required(login_url=('/login/'))
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.user != address.user:
        return redirect('request:my_addresses')
    form = AddressForm(request.POST or None, instance=address)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('request:my_addresses')
    return render(request, 'request/edit_address.html', {'form': form})

@login_required(login_url=('/login/'))
def my_notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'request/my_notifications.html', {'nots': notifications})

    
