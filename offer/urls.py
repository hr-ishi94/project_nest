from django.urls import path
from . import views


urlpatterns = [
    path('offer/',views.offer,name='offer'),
    path('add_offer/',views.add_new_offer,name='add_new_offer'),
    path('delete_offer/<int:delete_id>',views.delete_offer,name='delete_offer'),
    path('edit_offer/<int:edit_id>',views.edit_offer,name='edit_offer')
]
