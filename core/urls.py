from django.urls import path
from . import views



urlpatterns = [
    
    path('',views.index,name='index'),
    path('product_show/<int:prod_id>/<int:img_id>',views.product_show,name='product_show'),
    path('search_view/',views.search_view,name='search_view'),
]
