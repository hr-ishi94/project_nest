from django.urls import path
from . import views

urlpatterns=[
 
       path('checkout/',views.checkout,name='checkout'),
       path('placeorder/',views.placeorder,name='placeorder'),
       path('proceedtopay/', views.razarypaycheck, name = 'razarypaycheck'),
       path('order_invoice/<int:invoice_id>', views.order_invoice, name = 'order_invoice'),

]