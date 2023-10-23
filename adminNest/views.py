from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from user.models import *
from django.db.models import Q
from products.models import ProductReview

from checkout.models import OrderItem,Order
from django.db.models import Sum
from datetime import datetime,date

def admin_login1(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        if username.strip()=='' or password.strip()=='':
            messages.error(request,'fields cannot be empty!')
            return redirect('admin_login1')
        user=authenticate(username=username,password=password)

        if user is not None:
            
            if user.is_active:
               if user.is_superuser:
                    login(request,user)
                    return redirect('dashboard')
               else:
                    messages.warning(request,'Sorry only admin is allowed to login! ')
                    return redirect('admin_login1')
            else:
               messages.warning(request,"Your account has been blocked!")
               return redirect('admin_login1')

        else:
            messages.error(request,'Invalid username or password!')
            return render(request,'admin_login1')

    return render(request,'adminNest/admin_login1.html')


@login_required(login_url='admin_login1')
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    sales_data=OrderItem.objects.values('order__created_at__date').annotate(total_sales=Sum('price')).order_by('-order__created_at__date')
    categories=[item['order__created_at__date'].strftime('%d/%m') for item in sales_data]
    sales_values=[item['total_sales'] for item in sales_data]
    orders=Order.objects.order_by('-created_at')[:10]

    try:
        totalsale=0
        total_sales=Order.objects.all()
        for i in total_sales:
            i.total_price
            totalearnings+=i.total_price
    except:
        totalsale=0
    
    try:
        totalearnings=0
        total_earn=Order.objects.filter(order_status__id=4)
        for i in total_earn:
            i.total_price
            totalearnings+=i.total_price
    except:
        totalearnings=0

    try:
        status_delivery=Order.objects.filter(order_status__id=4).count()
        status_cancel=Order.objects.filter(order_status__id=5).count()
        Total=status_delivery +status_cancel
        status_delivery=(status_delivery/Total)*100
        status_cancel=(status_cancel/Total)*100
    except:
        status_delivery=0
        status_cancel=0


    
    context={
        'totalsale':totalsale,
        'totalearnings':totalearnings,
        'status_delivery':status_delivery,
        'status_cancel':status_cancel,
        'orders':orders,
        'categories':categories,
        'sales_values':sales_values,
        

    }


    return render(request,'adminNest/dashboard.html',context)

@login_required(login_url='admin_login1')
def usermanagement_1(request):
    users = CustomUser.objects.all().order_by('id')
    return render(request,'adminNest/usermanagement.html',{'users':users})


@login_required(login_url='admin_login1')   
def blockuser(request,user_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    user =CustomUser.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()  
    else:
        user.is_active = True
        user.save()
    return redirect('usermanagement_1')

@login_required(login_url='admin_login1')
def user_sort(request):
    search= request.POST.get('search')
    if search is None or search.strip()=='':
        messages.error(request,'Field cannot be empty! ')
        return redirect('usermanagement_1')
    users=CustomUser.objects.filter(Q(first_name__icontains=search)|Q(email__icontains=search)|Q(phone_number__icontains=search))
    if users:
        pass
    else:
        messages.error(request,'Search not found!')
        return redirect('usermanagement_1')
    return render(request,'adminNest/usermanagement.html',{'users':users})

@login_required(login_url='admin_login1')
def user_block_status(request):
    name=request.POST.get('name')
    if name=='Active':
        users=CustomUser.objects.filter(is_active=True)
        return render(request,'adminNest/usermanagement.html',{'users':users})
    if name=='Blocked':
        users=CustomUser.objects.filter(is_active=False)
        return render(request,'adminNest/usermanagement.html',{'users':users})
    if name=='All':
        users=CustomUser.objects.all()
        return render(request,'adminNest/usermanagement.html',{'users':users})
    else:
        return render(request,'adminNest/usermanagement.html')

@login_required(login_url='admin_login1')    
def admin_review(request):
    reviews=ProductReview.objects.all()
    
    return render(request,'adminNest/admin_review.html',{'reviews':reviews})


@login_required(login_url='admin_login1')
def admin_logout1(request):
    logout(request)
    return redirect('admin_login1')

@login_required(login_url='admin_login1')
def sales_report(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    if request.method=='GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
    
        if start_date and end_date:
            # Filter orders based on the selected date range
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date > end_date:
                messages.error(request, "Start date must be before end date.")
                return redirect('sales_report')
            if end_date > date.today():
                messages.error(request, "End date cannot be in the future.")
                return redirect('sales_report')

            orders = Order.objects.filter(created_at__date__range=(start_date, end_date))
            recent_orders = orders.order_by('-created_at')
        else:
            # If no date range is selected, fetch recent 10 orders
            recent_orders = Order.objects.order_by('-created_at')[:10]
            orders = Order.objects.all()
  
    # Calculate total sales and total orders
    total_sales = sum(order.total_price for order in orders)
    total_orders = orders.count()

    # Calculate sales by status
    sales_by_status = {
        'Pending': orders.filter(order_status= 1).count(),
        'Processing': orders.filter(order_status=2).count(),
        'Shipped': orders.filter(order_status=3).count(),
        'Delivered': orders.filter(order_status=4).count(),
        'Cancelled': orders.filter(order_status=5).count(),
        'Return': orders.filter(order_status=6).count(),
    }
    # Prepare data for rendering the template
    sales_report = {
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
        'total_sales': total_sales,
        'total_orders': total_orders,
        'sales_by_status': sales_by_status,
        'recent_orders': recent_orders,
    }

    return render(request, 'adminNest/salesreport.html', {'sales_report': sales_report})



 