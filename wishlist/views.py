from django.shortcuts import render,redirect
from .models import Wishlist
from variant.models import VariantImage
from products.models import Size
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='user_login1')
def wish_list(request):
    if request.user.is_authenticated:
        wishlist=Wishlist.objects.filter(user=request.user).order_by('id')
        variants=wishlist.values_list('variant',flat=True)
        img=VariantImage.objects.filter(variant__in=variants).distinct('variant')
        # cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        size=Size.objects.all()

        context={
            'wishlist':wishlist,
            'img':img,
            'size':size,
            # 'cart_count':cart_count,
            'wishlist_count':wishlist_count,

        }
        return render(request,'wishlist/wishlist.html',context)
    else:
        return render(request,'wishlist/wishlist.html')

def add_wish_list(request):
    if request.method=='POST':
        if request.user.is_authenticated:

            variant_id= request.POST.get('variant_id')
            add_size=request.POST.get('add_size')

            if Wishlist.objects.filter(user=request.user,variant_id=variant_id).exists():
                return JsonResponse({'status':'Product already in Wishlist'})
            
            else:
                Wishlist.objects.create(user=request.user,variant_id=variant_id)
                return JsonResponse({'status':'Product added successfully in wishlist'})

        else:
            return JsonResponse({'status':'You are not logged in please Login to continue!'})  


    return redirect('index')  

# @login_required(login_url='user_login1')
def remove_wish_list(request,wish_id):

    try :
        Wishlist_remove=Wishlist.objects.get(id=wish_id)
        Wishlist_remove.delete()
        messages.success(request,'Product removed from wishlist successfully!')
    except:
        return redirect('wish_list')

    return redirect('wish_list')        



    
