from categories.models import category
from cart.models import Cart
from wishlist.models import Wishlist
from userprofile.models import Wallet
from django.db.models import Sum


def default(request):
    categories=category.objects.all()
   
    try:
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        wallet=Wallet.objects.filter(user=request.user)
        total_balance=wallet.aggregate(Sum('wallet'))['wallet__sum']   
    except:
        cart_count= False
        wishlist_count=False  
        wallet=False 
        total_balance=0

      
    return {
        'categories':categories,
        'cart_count':cart_count,
        'wishlist_count':wishlist_count,
        'total_balance':total_balance

    }