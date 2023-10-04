from django.shortcuts import render,HttpResponse,redirect
from variant.models import VariantImage
from products.models import Size,ProductReview,Product
from django.db.models import Avg
from categories.models import category



def index(request):
    
    categories=category.objects.all()
    products=Product.objects.all()
    variant_images=VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product')
    context={
        'categories':categories,
        'products':products,
        'variant_images':variant_images
    }

   

    
    return render(request,'core/index.html',context)

def product_show(request,prod_id,img_id):
  
    variant = VariantImage.objects.filter(variant=img_id,is_available=True)
    variant_images = (VariantImage.objects.filter(variant__product__id=prod_id,is_available=True)
                     .distinct('variant__product'))
    # size =VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__size')
    size =Size.objects.all()
    color=VariantImage.objects.filter(variant__product__id=prod_id,is_available=True).distinct('variant__color')
    
    # reviews = ProductReview.objects.filter(product=prod_id)
    # average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    # rev_count=ProductReview.objects.filter(product=prod_id).count()
    # try:
    #     cart_count =Cart.objects.filter(user =request.user).count()
    #     wishlist_count =Wishlist.objects.filter(user=request.user).count()
    # except:
    #     cart_count =False
    #     wishlist_count =False 
    # try:
    #  average_rating = int(average_rating)
    # except:
    #     average_rating=0
    context={
        'variant':variant,
        'size':size,
        'color':color,
        'variant_images' :variant_images,    
        # 'reviews':reviews,
        # 'average_rating':average_rating ,
        # 'rev_count':rev_count,
        # 'wishlist_count':wishlist_count,
        # 'cart_count' :cart_count,
    }
 
    return render(request,'products/products_show.html',context)   



