from django.db import models
from user.models import CustomUser

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50,blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50,blank=True)
    state = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)
    pincode = models.CharField(max_length=50,blank=True)
    order_note = models.CharField(max_length=100, blank=True ,null=True)
    is_available =models.BooleanField(null=True,default=True)

    def __str__(self):
        return f"{self.id}"

class Wallet(models.Model):
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    wallet= models.PositiveBigIntegerField(null=True)