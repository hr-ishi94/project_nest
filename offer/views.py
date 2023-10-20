from django.shortcuts import render,redirect
from offer.models import Offer
from django.contrib import messages

from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(login_url='admin_login1')
def offer(request):
    offer=Offer.objects.filter(is_available=True).order_by('id')

    return render(request,'adminNest/offer.html',{'offer':offer})

@login_required(login_url='admin_login1')
def add_new_offer(request):
    if request.method=='POST':
        offername=request.POST.get('offername')
        discount=request.POST.get('discount')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')

        if offername is None or offername.strip()=='':
            messages.error(request,'Field Should not empty!')
            return redirect('offer')
        if discount is None or discount.strip()=='':
            messages.error(request,'Field Should not empty!')
            return redirect('offer')
        try:
            start_date=datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date=datetime.strptime(end_date,'%Y-%m-%d').date()
        except ValueError:
            messages.error(request,'Invalid date format. Use YYYY-MM-DD.!')
            return redirect('offer')

        if start_date>=end_date:
            messages.error(request,'Start date must be before end date.')
            return redirect('offer')

        if start_date< timezone.now().date():
            messages.error(request,'Enter valid start date.')
            return redirect('offer')        

        

        offer=Offer.objects.create(
            offer_name=offername,
            discount_amount=discount,
            start_date=start_date,
            end_date=end_date,


        )
        offer.save()
        messages.success(request,'Offer successfully added!')

    return redirect('offer')

@login_required(login_url='admin_login1')
def delete_offer(request,delete_id):
    try:    
        offer=Offer.objects.get(id=delete_id)
        offer.is_available=False
        offer.save()
        messages.success(request,'Offer successfully deleted!')
    except offer.DoesNotExist:
        messages.error(request,'Offer doesnot exist!')

    return redirect('offer')


@login_required(login_url='admin_login1')
def edit_offer(request,edit_id):
    if request.method == 'POST':
        offername = request.POST.get('offername')
        discount = request.POST.get('discount')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if offername is None or offername.strip() == '':
            messages.error(request, "Order name cannot be blank.")
            return redirect('offer')
        if discount.strip() == '':
            messages.error(request, "Cannot blank Offer field")
            return redirect('offer')
        if Offer.objects.filter(offer_name=offername ,is_available=True).exclude(id=offer_id).exists():
            messages.error(request, 'Offer name already exists')
            return redirect('offer')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect('offer')
        if start_date >= end_date:
            messages.error(request, "Start date must be before end date.")
            return redirect('offer')
        if start_date < timezone.now().date():
            messages.error(request, "Start date cannot be in the past.")
            return redirect('offer')
        
        off = Offer.objects.get(id=edit_id)
        off.offer_name = offername
        off.discount_amount = discount
        off.start_date = start_date
        off.end_date = end_date
        off.save()
        messages.success(request, "Offer edited successfully!")
        return redirect('offer')
    offers : Offer.objects.get(id=edit_id)
    context ={ 
     'offer':offers,
    }
    return render(request, 'adminside/offer.html', context)