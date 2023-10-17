from django.urls import path
from . import views

urlpatterns=[
  path('', views.categories, name='categories'),
  path('add_category/', views.add_category, name='add_category'),
  path('category_search/', views.category_search, name='category_search'),
  path('editcategory/<slug:editcategory_id>', views.editcategory, name='editcategory'),
  path('deletecategory/<slug:deletecategory_id>', views.deletecategory, name='deletecategory'),
  path('category_view/',views.category_view,name='category_view'),
  path('category_product_view/<slug:c_id>',views.category_product_view,name='category_product_view'),

]
     

