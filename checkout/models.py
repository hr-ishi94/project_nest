from django.db import models
from coupon.models import Coupon
from userprofile.models import Address
from variant.models import VariantImage,Variant
from user.models import CustomUser
from datetime import timedelta, timezone
# # Create your models here.

class Orderstatus(models.Model):
    order_status = models.CharField(max_length=60)

    def __str__(self):
        return self.order_status
class Itemstatus(models.Model):
    item_status = models.CharField(max_length=60)

    def __str__(self):
        return self.item_status
    
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null= False)
    payment_id = models.CharField(max_length=250, null=True)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    order_status = models.ForeignKey(Orderstatus, on_delete=models.CASCADE ,null=True,default=1)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True )
    return_total_price=models.IntegerField(null=True)

    @property
    def expected_delivery(self):
        return self.created_at + timedelta(days=4)
    

    def __str__(self):
        return f"{self.id, self.tracking_no}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    orderitem_status = models.ForeignKey(Itemstatus, on_delete=models.CASCADE,null=True,default=1)
    
    


    def __str__(self):
        return f"{self.order.id, self.order.tracking_no}"

class OrderAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=50, blank=True)
    order_note = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

         