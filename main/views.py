from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
#rest APIs
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, GroupSerializer


def mylogin(request):
    if request.method == 'POST':
        #Making an authentication form and checking it is valid
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #authenticate returns User object if username and password are correct
            user = authenticate(username=username, password=password)
            
            if user is not None:
                #login if everything is correct
                login(request, user)
                return redirect('items:index')
            else:
                return render(request, 'main/login.html', {'form': form})
        
        else:
            return render(request, 'main/login.html', {'form': form})
    if request.user.is_authenticated:
        return redirect('items:index')    
    form = AuthenticationForm
    return render(request, 'main/login.html', {'form': form})

def mylogout(request):
    logout(request)
    return redirect('items:index')

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('merchant') == 'Yes':
                merchant_group = Group.objects.get(name='Merchant')
                merchant_group.user_set.add(user)
            login(request, user)
            return redirect('items:index')
        else:
            return render(request, 'main/register.html', {'form': form})
    if request.user.is_authenticated:
        return redirect('items:index')
    form = NewUserForm()
    return render(request, 'main/login.html', {'form': form})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
