from django.shortcuts import render
from django.urls import reverse
from variant.models import VariantImage,Variant
from products.models import Size,ProductReview,Product
from django.db.models import Avg,Min,Max
from categories.models import category
from cart.models import *
from wishlist.models import *

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect    
from django.template.loader import render_to_string
from .forms import PriceRangeForm
from django.core import serializers
import json
from django.db.models import Q,F, Min,Max       


def index(request):
    categories = category.objects.all()
    products = Product.objects.all()
    
    # Retrieve the minimum and maximum prices
    min_price = Product.objects.aggregate(Min('product_price'))
    max_price = Product.objects.aggregate(Max('product_price'))
    
    variant_images = VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product')
    
    p = Paginator(VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product'), 5)
    page = request.GET.get('page')
    product_page = p.get_page(page)
    nums = "a" * product_page.paginator.num_pages
    
    filtered_products = request.session.get('filtered_products', [])

    # Check if filtered_products is not an empty list
    if filtered_products:
        # Extract product IDs from the list of dictionaries
        filtered_product_ids = [item.get('id') for item in filtered_products if 'id' in item]
        
        # Use the extracted product IDs to filter products
        filtered_products = Product.objects.filter(id__in=filtered_product_ids)
    else:
        # If there are no filtered products, display all products
        filtered_products = Product.objects.all()
    
    context = {
        'categories': categories,
        'products': products,
        'variant_images': variant_images,
        'product_page': product_page,
        'nums': nums,
        'min_price': min_price,
        'max_price': max_price,
        'filtered_products': filtered_products,  # Send filtered products to the template
    }
    
    return render(request, 'core/index.html', context)

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


def filter_data(request):
    if request.method == 'POST':
        form = PriceRangeForm(request.POST)
        if form.is_valid():
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']

            print("Min Price:", min_price)
            print("Max Price:", max_price)

            # Filter products based on the price range
            filtered_products = Product.objects.filter(
                Q(product_price__gte=min_price) & Q(product_price__lte=max_price)
            )
            print("Filtered products:", filtered_products)

            # Convert the QuerySet to a list of dictionaries
            filtered_products_data = json.loads(serializers.serialize('json', filtered_products))

            # Store the filtered products in the session
            request.session['filtered_products'] = filtered_products_data

    return HttpResponseRedirect(reverse('index'))


def error_404_view(request,exception):
    return render(request,'404.html')





