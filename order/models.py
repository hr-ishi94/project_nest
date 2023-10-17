from django.db import models

from checkout.models import Order
from user.models import CustomUser

class Order_Cancelled(models.Model):
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete= models.CASCADE)
    options=models.CharField(max_length=100,null=True)
    reason=models.TextField(null=True)

