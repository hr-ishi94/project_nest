from django.shortcuts import render,HttpResponse,redirect
from variant.models import VariantImage,Variant
from products.models import Size,ProductReview,Product
from django.db.models import Avg
from categories.models import category
from cart.models import *
from wishlist.models import *

from django.core.paginator import Paginator



def index(request):
    
    categories=category.objects.all()
    products=Product.objects.all()
    
    variant_images=VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product')
    p=Paginator(VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product'), 5)
    page=request.GET.get('page')
    product_page=p.get_page(page)
    nums="a"*product_page.paginator.num_pages
    
    context={
        'categories':categories,
        'products':products,
        'variant_images':variant_images,
        'product_page':product_page, 
        'nums':nums
    }

   

    
    return render(request,'core/index.html',context)

def product_show(request,prod_id,img_id):
  
    variant = VariantImage.objects.filter(variant=img_id,is_available=True)
    variant_images = (VariantImage.objects.filter(variant__product__id=prod_id,is_available=True)
                     .distinct('variant__product'))
    size =VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__size')
    size =Size.objects.filter(is_available=True)
    color=VariantImage.objects.filter(variant__product__id=prod_id,is_available=True).distinct('variant__color')
    
    reviews = ProductReview.objects.filter(product=prod_id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    # rev_count=ProductReview.objects.filter(product=prod_id).count()
    # count_rev=ProductReview
    product=Product.objects.get(id=prod_id)
    disc=round((product.offer.discount_amount/product.product_price)*100)
    try:
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count =False
        wishlist_count =False 
    try:
     average_rating = int(average_rating)
    except:
        average_rating=0
    context={
        'variant':variant,
        'size':size,
        'color':color,
        'variant_images' :variant_images,    
        'wishlist_count':wishlist_count,
        'cart_count' :cart_count,
        'reviews':reviews,
        'average_rating':average_rating ,
        'disc':disc
        # 'rev_count':rev_count,
    }
 
    return render(request,'products/products_show.html',context) 

def search_view(request):
    query=request.GET.get('query')
    variant_images=(VariantImage.objects.filter(variant__product__product_name__icontains=query,is_available=True).distinct('variant__product__product_name'))
    try:
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count=False
        wishlist_count=False
    
    context={
        'variant_images':variant_images,
        'wishlist_count':wishlist_count,
        'cart_count':cart_count,
        'query':query
    }    

    return render(request,'core/search.html',context)  



