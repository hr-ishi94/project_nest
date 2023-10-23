from django.urls import path
from . import views

urlpatterns = [
    path('usermanagement_1/',views.usermanagement_1,name='usermanagement_1'),
    path('admin_login1/',views.admin_login1,name='admin_login1'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('blockuser/<int:user_id>/',views.blockuser,name='blockuser'),
    path('user_sort/',views.user_sort,name='user_sort'),
    path('user_block_status/',views.user_block_status,name='user_block_status'),
    path('admin_logout1/',views.admin_logout1,name='admin_logout1'),
    path('admin/user_reviews/',views.admin_review,name='admin_review'),
    path('sales_report/',views.sales_report,name='sales_report'),
    
    
]
