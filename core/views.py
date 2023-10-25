from django.shortcuts import render
from variant.models import VariantImage,Variant
from products.models import Size,ProductReview,Product
from django.db.models import Avg,Min,Max
from categories.models import category
from cart.models import *
from wishlist.models import *

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import PriceRangeForm



def index(request):
    
    categories=category.objects.all()
    products=Product.objects.all()
    min_price=Product.objects.aggregate(Min('product_price'))
    max_price=Product.objects.aggregate(Max('product_price'))
    


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
        'nums':nums,
        'min_price':min_price,
        'max_price':max_price,
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


# def filter_data(request):
#     min=request.GET['minPrize']
#     max=request.GET['maxPrize']
#     allProducts= Product.objects.all().order_by('-id').distinct()
#     allProducts=allProducts.filter(product_price__gte=min)
#     allProducts=allProducts.filter(product_price__lte=max)
#     t=render_to_string('ajax/product-list.html',{'data':allProducts})
#     return JsonResponse({'data':t})


from django.http import HttpResponseRedirect
from django.urls import reverse

def filter_data(request):
    if request.method == 'POST':
        form = PriceRangeForm(request.POST)
        if form.is_valid():
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']
            
            # Store the filter criteria in the session
            request.session['filter_min_price'] = min_price
            request.session['filter_max_price'] = max_price

    # Redirect back to the index view
    return HttpResponseRedirect(reverse('index'))


def error_404_view(request,exception):
    return render(request,'404.html')





