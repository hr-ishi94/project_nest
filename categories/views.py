from django.shortcuts import render, redirect
import logging

from products.models import Product
from variant.models import Variant,VariantImage
from .models import category
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required(login_url='admin_login1')
def categories(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    categories = category.objects.filter(is_available=True).order_by('id')
    p=Paginator(categories,5)
    page=request.GET.get('page')
    product_page=p.get_page(page)
    page_nums='a'*product_page.paginator.num_pages
    return render(request, 'category/category.html', {'categories': categories,'product_page':product_page,
        'page_nums':page_nums})

@login_required(login_url='admin_login1')
def add_category(request):
    try:
        if not request.user.is_superuser:
            return redirect('admin_login1')

        if request.method == 'POST':
            image = request.FILES.get('image', None)
            name = request.POST['categories']
            description = request.POST['categories_discription']
            
            # Validation
            if name.strip() == '':
                messages.error(request, 'Name Not Found!')
                return redirect('categories')

            if category.objects.filter(categories=name).exists():
                messages.error(request, 'Category name already exists')
                return redirect('categories')
            # Save
            if not image:
                messages.error(request, 'Image not uploaded')
                return redirect('categories')

            new_category = category(categories=name, categories_discription=description, categories_image=image)
            new_category.save()
            messages.success(request,'category added successfully!')
            return redirect('categories')
    except:
        
            return redirect('categories')

@login_required(login_url='admin_login1')
def editcategory(request, editcategory_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method == 'POST':
        name = request.POST['categories']
        description = request.POST['categories_discription']

# validation
        try:
            caterg = category.objects.get(slug=editcategory_id)
            image = request.FILES.get('image')
            if image:
                caterg.categories_image = image
                caterg.save()
        except category.DoesNotExist:
            messages.error(request,'Image Not Fount')
            return redirect('categories')
        if name.strip() == '':
            messages.error(request,'Name field is empty')
            return redirect('categories')
        if category.objects.filter(categories=name).exists():
            check = category.objects.get(slug = editcategory_id)
            if name == check.categories:
                pass
            else:
                messages.error(request, 'category name already exists')
                return redirect('categories')
        
        categr = category.objects.get(slug=editcategory_id)
        categr.categories = name
        categr.slug = name
        categr.categories_discription = description
        categr.save()
        messages.success(request,'category edited successfully!')
        return redirect ('categories')

@login_required(login_url='admin_login1')
def deletecategory(request,deletecategory_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    categery = category.objects.get(id=deletecategory_id)
    products = Product.objects.filter(category=categery)
    for product in products:
        product.is_available = False
        product.save()

    variants = Variant.objects.filter(product=product)
    for variant in variants:
        variant.is_available = False
        variant.quantity = 0
        variant.save()

    categery.is_available = False
    categery.save()

    messages.success(request,'category deleted successfully!')
    return redirect('categories')

@login_required(login_url='admin_login1')
def category_search(request):
    search = request.POST.get('search')
    if search is None or search.strip() == '':
        messages.error(request,'Filed cannot empty!')
        return redirect('categories')
    categories = category.objects.filter(categories__icontains=search,is_available=True )
    if categories :
        pass
        return render(request, 'category/category.html', {'categories': categories})
    else:
        categories:False
        messages.error(request,'Search not found!')
        return redirect('categories')

def category_view(request):
    catg=category.objects.filter(is_available=True)
    context={
        'category':catg
    }
    return render(request,'category/category_view.html',context)

def category_product_view(request, c_id):
    category_instance = category.objects.get(id=c_id)

    variant = VariantImage.objects.filter(variant__product__category__id=c_id,variant__product__is_available=True).order_by('variant__product').distinct('variant__product')
    
    context = {
        'category': category_instance,
        'variant': variant

        
    }
    return render(request, 'category/category_product_view.html', context)





  


        
       

        
