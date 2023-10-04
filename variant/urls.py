from django.urls import path
from . import views

urlpatterns=[
        path('product_variant/',views.product_variant,name='product_variant'),
        path('product_size/',views.product_size,name='product_size'),
        path('add_size/',views.add_size,name='add_size'),
        path('size_delete/<int:size_range_id>',views.size_delete,name='size_delete'),
        path('product_color/',views.product_color,name='product_color'),
        path('add_color/',views.add_color,name='add_color'),
        path('variant_search/',views.variant_search,name='variant_search'),
        path('color_delete/<int:color_name_id>/',views.color_delete,name='color_delete'),
        path('add_Product_Variant/',views.add_Product_Variant,name='add_Product_Variant'),
        path('edit_productvariant/<int:variant_id>/',views.edit_productvariant,name='edit_productvariant'),
        path('productvariant_delete/<int:variant_id>/',views.productvariant_delete,name='productvariant_delete'),
        path('image_view/<int:img_id>/',views.image_view,name='image_view'),
        path('image_list/<int:variant_id>/',views.image_list,name='image_list'),
        path('image_delete/<int:image_id>/',views.image_delete,name='image_delete'),
        path('product_variant_view/<int:product_id>/',views.product_variant_view,name='product_variant_view'),

]





