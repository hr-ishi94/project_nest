from django.urls import path
from . import views



urlpatterns = [
    
    path('',views.index,name='homepage'),
    path('product_show/<int:prod_id>/<int:img_id>',views.product_show,name='product_show'),
]
