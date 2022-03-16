from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from items.models import Item

class Gov(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

class Address(models.Model):
    class Meta:
        verbose_name_plural = 'Addresses'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gov = models.ForeignKey(Gov, on_delete=models.CASCADE)
    dis = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    mark = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.gov.name + " , " + self.street

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    #Return total price per object Order
    def tot_price(self):
        return self.item.price * self.quantity
    
    #Get the order item image for the template
    def get_item_img(self):
        return self.item.img

    def __str__(self):
        return self.item.name + ", by: " + self.item.user.username + ", " + str(self.quantity)

class Cashout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merchant')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address', null=True)

    def __str__(self):
        return self.buyer.username + " ordered: " + self.order.item.name