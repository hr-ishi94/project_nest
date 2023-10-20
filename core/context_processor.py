from categories.models import category
from cart.models import Cart
from wishlist.models import Wishlist
from userprofile.models import Wallet


def default(request):
    categories=category.objects.all()
    wallet=Wallet.objects.all()
    try:
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count= False
        wishlist_count=False    
    return {
        'categories':categories,
        'cart_count':cart_count,
        'wishlist_count':wishlist_count,
        'wallet':wallet

    }