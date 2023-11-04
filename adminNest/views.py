from itertools import groupby
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from user.models import *
from django.db.models import Q
from products.models import ProductReview

from checkout.models import OrderItem,Order
from django.db.models import Sum,Prefetch
from datetime import datetime,date
import csv
from fpdf import FPDF


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
            return redirect('admin_login1')

    return render(request,'adminNest/admin_login1.html')


@login_required(login_url='admin_login1')
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    sales_data = OrderItem.objects.values('order__created_at__date').annotate(total_sales=Sum('price')).order_by('-order__created_at__date')
    # Prepare data for the chart
    categories = [item['order__created_at__date'].strftime('%d/%m') for item in sales_data]
    sales_values = [item['total_sales'] for item in sales_data]
    
   
    return_data = OrderItem.objects.filter(orderitem_status__item_status__in=["Return", "Cancelled"]).values('order__created_at__date').annotate(total_returns=Sum('price')).order_by('-order__created_at__date')
    return_values = [item['total_returns'] for item in return_data]
    orders =Order.objects.order_by('-created_at')[:10]
    try:
        totalsale=0
        total_sales =Order.objects.all()
        for i in total_sales:
            i.total_price
            totalsale+=i.total_price
    except:
         totalsale=0 
    try:
        totalearnings=0
        total_earn =Order.objects.filter(order_status__id=4)
        for i in total_earn:
            i.total_price
            totalearnings+=i.total_price
    except:
         totalearnings=0       
        
    try:
        status_pending_count=Order.objects.filter(order_status__id=1).count()
        status_delivery_count=Order.objects.filter(order_status__id=4).count()
        status_cancel_count =Order.objects.filter(order_status__id=5).count()
        status_return_count =Order.objects.filter(order_status__id=6).count()
        Total = status_delivery_count + status_cancel_count + status_return_count
        status_delivery = (status_delivery_count / Total) * 100
        status_cancel = (status_cancel_count / Total) * 100
        status_return = (status_return_count / Total) * 100
    except:
        # status_pending_count=0
        # status_delivery_count=0
        # status_cancel_count=0
        # status_return_count=0
        status_delivery=0
        status_cancel=0
        status_return=0
        
            
    context = {
        'delivery_count':status_delivery_count,
        'cancel_count':status_cancel_count,
        'pending_count':status_pending_count,

        'totalsale':totalsale,
        'totalearnings':totalearnings,
        'status_delivery':status_delivery,
        'status_cancel':status_cancel,
        'status_return':status_return,
        'orders':orders,
        'categories': categories,
        'sales_values': sales_values,
        'return_values': return_values,
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

@login_required(login_url='admin_login1')
def export_csv(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no', 'Orderd at', 'product_name', 'product_price', 'product_quantity'])

    orders = Order.objects.all()
    for order in orders:
        order_items = OrderItem.objects.filter(order=order).select_related('variant')  # Use select_related to optimize DB queries
        grouped_order_items = groupby(order_items, key=lambda x: x.order_id)
        for order_id, items_group in grouped_order_items:
            items_list = list(items_group)
            for order_item in items_list:
                writer.writerow([
                    order.user.first_name if order_item == items_list[0] else "",
                    order.total_price if order_item == items_list[0] else "",
                    order.payment_mode if order_item == items_list[0] else "",
                    order.tracking_no if order_item == items_list[0] else "",
                    order.created_at if order_item == items_list[0] else "",  # Only include date in the first row
                    order_item.variant.product.product_name,  # Replace 'product_name' with the actual attribute in your Product model
                    order_item.price,
                    order_item.quantity,
                ])

    return response


from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from django.shortcuts import redirect
from django.db.models import Prefetch
from checkout.models import Order, OrderItem


from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def generate_pdf(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=SalesReport' + str(datetime.now()) + '.pdf'
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    # Header Information
    elements.append(Paragraph('Sales Report', style=getSampleStyleSheet()['Title']))
    elements.append(Paragraph(str(datetime.now()), style=getSampleStyleSheet()['Normal']))
    elements.append(Paragraph('<br/><br/>', style=getSampleStyleSheet()['Normal']))

    data = [['User', 'Total Price', 'Payment Mode', 'Tracking No', 'Ordered At', 'Product Name', 'Product Price', 'Product Quantity']]
    orders = Order.objects.all().prefetch_related(
        Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('variant'))
    )
    total_sales = sum(order.total_price for order in orders)
    total_orders = orders.count()

    for order in orders:
        order_items = order.orderitem_set.all()
        total_sales += order.total_price
        total_orders += 1
        for index, order_item in enumerate(order_items):
            data.append([
                order.user.first_name if index == 0 else "",
                'Rs.' + str(order.total_price) if index == 0 else "",
                order.payment_mode if index == 0 else "",
                order.tracking_no if index == 0 else "",
                str(order.created_at.date()) if index == 0 else "",
                order_item.variant.product.product_name,
                'Rs.' + str(order_item.price),
                order_item.quantity,
            ])

    # Create a table with data
    table = Table(data)

    # Add style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    elements.append(table)

    elements.append(Paragraph('<br/><br/>', style=getSampleStyleSheet()['Normal']))
    # Add Total Sales and Total Orders
    elements.append(Paragraph(f'Total Sales: Rs. {total_sales}', style=getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f'Total Orders: {total_orders}nos.', style=getSampleStyleSheet()['Normal']))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

 