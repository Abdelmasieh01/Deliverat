from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    #Item describtion
    des = models.CharField(max_length=1500)
    price = models.FloatField(default=0.0)
    #Upload the image to subfolder items in media folder
    img = models.ImageField(upload_to='items')
    #The score (how many time they are bought) by which the items will be ordered
    score = models.IntegerField(default=0)
    #How many items are available in stock
    stock = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    #return the item + merchant name
    def __str__(self):
        return self.name
    
    def return_username(self):
        return self.user.username
