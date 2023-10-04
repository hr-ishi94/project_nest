from django.db import models
from user.models import CustomUser
from variant.models import Variant

class Cart(models.Model):
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    single_total = models.BigIntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
