from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from variant.models import *
from django.db.models import Q



@login_required(login_url='admin_login1')
def product(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    product=Product.objects.filter(is_available=True).order_by('id')

    product_list={
        'product':product,
        'categories':category.objects.filter(is_available=True).order_by('id'),
        'offer': Offer.objects.filter(is_available= True).order_by('id')

    }

    return render (request,'products/products.html',product_list)



@login_required(login_url='admin_login1')
def addproduct(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        category_id = request.POST.get('category')
        offer_id = request.POST.get('offer')
        product_description = request.POST.get('product_description')
        # Validation
        if Product.objects.filter(product_name=name).exists():
            check = Product.objects.get(product_name=name)
            if check.is_available == False:
                check.product_name +=check.product_name
                check.slug +=check.slug
                check.save()
            else:    
                messages.error(request, 'Product name already exists')
                return redirect('product')
      
        if name.strip() == '' or price.strip() == '':
            messages.error(request, "Name or Price field are empty!")
            return redirect('product')
       
        category_obj = category.objects.get(id=category_id)
        if offer_id == '':
            offer_obj=None
        else:    
            offer_obj = Offer.objects.get(id=offer_id)
        
       
        # Save        
        product = Product(
          
            product_name=name,
            category=category_obj,
            offer=offer_obj,
            product_price=price,
            slug=name,
            product_description=product_description,

        )
        product.save()
        messages.success(request,'product added successfully!')
        return redirect('product')
    
    return render(request, 'products/products.html')


@login_required(login_url='admin_url1')
def product_delete(request,product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    delete_product=Product.objects.get(id=product_id)
    variants=Variant.objects.filter(product=delete_product)
    for variant in variants:
        variant.is_available= False
        variant.quantity=0
        variant.save()
    delete_product.is_available=False
    delete_product.save()
    messages.success(request,'product deleted successfully!')
    return redirect('product') 

@login_required(login_url='admin_login1')
def product_edit(request,product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method=='POST':
        name=request.POST['product_name']
        price=request.POST['product_price']
        category_id=request.POST.get('category')
        offer_id=request.POST.get('offer')
        product_description = request.POST.get('product_description')

        if name.strip()=='' or price.strip()=='':
            messages.error(request,'Fields cannot be empty!')
            return redirect('product')
        
        category_obj= category.objects.get(id=category_id)
        if offer_id=='':
            offer_id=None
        else:
            offer_obj=Offer.objects.get(id=offer_id)   

        if Product.objects.filter(product_name=name).exists():
            check=Product.objects.get(id=product_id)
            if name==check.product_name:
                pass
            else:
                messages.error(request,'Product name already exists!')
                return redirect('product')

        editproduct=Product.objects.get(id=product_id)
        editproduct.product_name=name
        editproduct.product_price=price
        editproduct.category=category_obj
        editproduct.offer=offer_obj
        editproduct.product_description=product_description
        editproduct.save()
        messages.success(request,'Product edited successfully!')
        return redirect('product')

@login_required(login_url='admin_login1')
def product_search(request):
    search=request.POST.get('search')
    if search is None or search.strip()=='':
        messages.error(request,'Field cannot be empty')
        return redirect('product')
    product=Product.objects.filter(Q(product_name__icontains=search)|Q(product_price__icontains=search) | Q (category_categories__icaontains=search),is_available=True)
    product_list={
        'product':product,
        'categories':category.objects.filter(is_available=True).order_by('id')
    }
    if product:
        pass
        return render(request,'product/products.html',product_list)
    else:
        product: False
        messages.error(request,'Search not Found!')
        return redirect('product')
    
@login_required(login_url='admin_login1')
def product_view(request,product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    variant=Variant.objects.filter(product=product_id,is_available=True)
    size_range=Size.objects.filter(is_available=True).order_by('id')
    color_name=Color.objects.filter(is_available=True).order_by('id')
    product=Product.objects.filter(is_available=True).order_by('id')

    variant_list={
        'variant':variant,
        'size_range':size_range,
        'color_name':color_name,
        'product':product

    }

    return render(request,'View/product_view.html',{'variant_list':variant_list})

   
# def add_review(request):



















            


