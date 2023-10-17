from django.contrib import admin
from checkout.models import Order,Itemstatus, Orderstatus,OrderItem

admin.site.register(Order)
admin.site.register(Orderstatus)
admin.site.register(OrderItem)
admin.site.register(Itemstatus)
