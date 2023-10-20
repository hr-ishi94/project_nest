from django.shortcuts import render,redirect
from user.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Address
from cart.models import Cart
from wishlist.models import Wishlist
from checkout.models import Order,OrderItem,Itemstatus
from variant.models import VariantImage

from django.utils import timezone
from datetime import timedelta

# validators
from django.core.validators import validate_email
from django.forms import ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password


import re
@login_required(login_url='user_login1')
def userprofile(request):
    
    user = CustomUser.objects.get(email=request.user.email)
    address =Address.objects.filter(user=request.user,is_available=True )
    cart_count =Cart.objects.filter(user =request.user).count()
    wishlist_count =Wishlist.objects.filter(user=request.user).count()
    order =Order.objects.filter(user=request.user) 
    last_order=Order.objects.filter(user=request.user).last()
    try:
        wallet =Wallet.objects.get(user=request.user)
    except:
       wallet=0   

    context={
        'user1':user,
        'address':address,
        'wishlist_count':wishlist_count, 
        'cart_count':cart_count,
        'order':order,
        'wallet' :wallet,
        'last_order': last_order,
        
            
        }
    return render(request,'userprofile/userprofile.html',context)

def edit_profile(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(phone_number=request.user)    
        except:  
               return redirect('userprofile') 

        # print(phone_number,first_name)

        if phone_number == '':
            messages.error(request, 'phone_number is empty')
            return render(request,'userprofile/edit_profile.html',{'user':user})
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),phone_number ): 
            messages.error(request,'Enter valid phonenumber!')
            return render(request,'userprofile/edit_profile.html',{'user':user})
        phonenumber_checking=len(phone_number)
        if not  phonenumber_checking==10:
            messages.error(request,'phonenumber should be must contain 10digits!')  
            return render(request,'userprofile/edit_profile.html',{'user':user})
        if first_name.strip() == '' or last_name.strip() == '':
            messages.error(request, 'First or Lastname is empty')
            return render(request,'userprofile/edit_profile.html',{'user':user})
        if email.strip()=='':
            messages.error(request,'email cannot be empty')
            return render(request,'userprofile/edit_profile.html',{'user':user})
        email_check=validateemail(email)
        if email_check is False:
            messages.error(request,'email not valid!')
            return render(request,'userprofile/edit_profile.html',{'user':user})
            
      
        try:
            user = CustomUser.objects.get(phone_number=request.user)
            print(user)
            user.phone_number = phone_number
            user.first_name = first_name
            user.last_name = last_name
            user.email=email
            user.save()
            messages.success(request, 'userprofile updated successfully')
            return redirect('userprofile') 
            
        except:
            messages.error(request, 'User does not exist')
    try:
        user = CustomUser.objects.get(phone_number=request.user)    
    except:  
           return redirect('userprofile')       
    return render(request,'userprofile/edit_profile.html',{'user':user})
    
def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
    
def change_password(request):
    if request.method=='POST':
        old_password=request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        confirm_new_password=request.POST.get('confirm_new_password')

        if new_password.strip()=='' or confirm_new_password.strip()=='':
            messages.error(request,'field cannot be empty')
            return render(request,'userprofile/password.html')
        if new_password!=confirm_new_password:
            messages.error(request,"passwords didn't match")
            return render(request,'userprofile/password.html')
        password_check=validatepassword(new_password)
        if password_check is False:
            messages.error(request,'Password is not valid!')
            return render(request,'userprofile/password.html')
        user=CustomUser.objects.get(username=request.user)

        if check_password(old_password,user.password):
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request,user)
            messages.success(request,'Password updated successfully!')
            return redirect('userprofile')
        else:
            messages.error(request,'invalid old password')
            return render(request,'userprofile/password.html')

    return render(request,'userprofile/password.html')


def validatepassword(new_password):
    try:
        validate_password(new_password)
        return True
    except ValidationError:
        return False

def View_address(request,view_id):
    
    try:
        Viewaddress=Address.objects.get(id=view_id)
    except:
        return redirect('userprofile')
            
    
    return render(request,'userprofile/view_address.html',{'Viewaddress':Viewaddress})   

     

def add_address(request,add_id):

    if request.method == 'POST':
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
        

        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        country=request.POST.get('country')
        address=request.POST.get('address')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        state=request.POST.get('state')
        order_note=request.POST.get('order_note')
        
        context={
            'pre_first_name': first_name,
            'pre_last_name':last_name,
            'pre_country':country,
            'pre_address':address,
            'pre_city':city,
            'pre_pincode':pincode,
            'pre_phone':phone,
            'pre_email':email,
            'pre_state':state,
            'pre_order_note':order_note,
            'check':add_id,
            'wishlist_count':wishlist_count, 
            'cart_count':cart_count,
    
                }


        if request.user is None:
            return
        
        if first_name.strip() == '' : 
            messages.error(request,'names cannot be empty!!!')
            context['pre_first_name']=''
            return render(request,'userprofile/add_address.html',context)
            
        if last_name.strip() == '':
            messages.error(request,'names cannot be empty!!!')
            context['pre_last_name']=''
            return render(request,'userprofile/add_address.html',context)
        
        if country.strip()=='':
            messages.error(request,'Country cannot be empty')
            context['pre_country']=''
            return render(request,'userprofile/add_address.html',context)
        if city.strip()=='':
            messages.error(request,'city cannot be empty')
            context['pre_city']=''
            return render(request,'userprofile/add_address.html',context)
        if address.strip()=='':
            messages.error(request,'address cannot be empty')
            context['pre_address']=''
            return render(request,'userprofile/add_address.html',context)
        if pincode.strip()=='':
            messages.error(request,'pincode cannot be empty')
            context['pre_pincode']=''
            return render(request,'userprofile/add_address.html',context)
        if not re.search(re.compile(r'^\d{6}$'),pincode ):  
            messages.error(request,'should only 6 contain numeric!')   
            context['pre_pincode']=''
            return render(request,'userprofile/add_address.html',context)
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),phone): 
            messages.error(request,'Enter valid phonenumber!')
            context['pre_phone']=''
            return render(request,'userprofile/add_address.html',context)
        phonenumber_checking=len(phone)
        if not  phonenumber_checking==10:
            messages.error(request,'phonenumber should be must contain 10digits!')  
            context['pre_phone']=''
            return render(request,'userprofile/add_address.html',context)
                    
        if phone.strip()=='':
            messages.error(request,'phone cannot be empty')
            context['pre_phone']=''
            return render(request,'userprofile/add_address.html',context)
        if email.strip()=='':
            messages.error(request,'email cannot be empty')
            context['pre_email']=''
            return render(request,'userprofile/add_address.html',context)
        email_check=validateemail(email)
        if email_check is False:
            messages.error(request,'email not valid!')
            context['pre_email']=''
            return render(request,'userprofile/add_address.html',context)
                   
        if state.strip()=='':
            messages.error(request,'state cannot be empty')
            context['pre_state']=''
            return render(request,'userprofile/add_address.html',context)
        
        # ad =Address.objects.check()

        ads=Address()
        ads.user=request.user
        ads.first_name=first_name
        ads.last_name=last_name
        ads.country=country
        ads.address=address
        ads.city=city
        ads.pincode=pincode
        ads.phone=phone
        ads.email=email
        ads.state=state
        ads.order_note=order_note
        ads.is_available=True
        ads.save()
        messages.success(request,' Address Added successfully!')
        if add_id==1:
            check=1
            return redirect('userprofile')
        else: 
            check=2 
            return redirect('checkout')
        

    cart_count =Cart.objects.filter(user =request.user).count()
    wishlist_count =Wishlist.objects.filter(user=request.user).count()    
    if add_id==1:
        check=1
    else: 
        check=2    
    return render(request,'userprofile/add_address.html',{'check':check,'wishlist_count':wishlist_count,'cart_count':cart_count,})


def edit_address(request,edit_id):

    if request.method == 'POST':
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()

        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        country=request.POST.get('country')
        address=request.POST.get('address')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        state=request.POST.get('state')
        order_note=request.POST.get('order_note')
        try:
            editaddress=Address.objects.get(id=edit_id)
        except:
            return redirect('userprofile')

        if request.user is None:
            return
        
        if first_name.strip() == '' : 
            messages.error(request,'names cannot be empty!!!')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        if last_name.strip() == '':
            messages.error(request,'names cannot be empty!!!')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        if country.strip()=='':
            messages.error(request,'Country cannot be empty')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        if city.strip()=='':
            messages.error(request,'city cannot be empty')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        if address.strip()=='':
            messages.error(request,'address cannot be empty')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        if pincode.strip()=='':
            messages.error(request,'pincode cannot be empty')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        if not re.search(re.compile(r'^\d{6}$'),pincode ):  
            messages.error(request,'should only 6 contain numeric!')   
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),phone ): 
            messages.error(request,'Enter valid phonenumber!')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        if phone.strip()=='':
            messages.error(request,'phone cannot be empty')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        phonenumber_checking=len(phone)
        if not  phonenumber_checking==10:
            messages.error(request,'phonenumber should be must contain 10digits!')  
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        if email.strip()=='':
            messages.error(request,'email cannot be empty')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        email_check=validateemail(email)
        if email_check is False:
            messages.error(request,'email not valid!')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})     
        if state.strip()=='':
            messages.error(request,'state cannot be empty')
            return render(request,'userprofile/edit_address.html',{'editaddress':editaddress})
        try:
            ads = Address.objects.get(id=edit_id)
        except Address.DoesNotExist:
            messages.error(request, 'Address not found!')
            return redirect('userprofile')
        ads.user=request.user
        ads.first_name=first_name
        ads.last_name=last_name
        ads.country=country
        ads.address=address
        ads.city=city
        ads.pincode=pincode
        ads.phone=phone
        ads.email=email
        ads.state=state
        ads.order_note=order_note
        ads.is_available=True
        ads.save()
        messages.success(request,' Address Edited successfully!')

        return redirect('userprofile')
    try:
        editaddress=Address.objects.get(id=edit_id)
    except:
        return redirect('userprofile')
    cart_count =Cart.objects.filter(user =request.user).count()
    wishlist_count =Wishlist.objects.filter(user=request.user).count()        
    return render(request,'userprofile/edit_address.html',{'editaddress':editaddress, 'wishlist_count':wishlist_count,'cart_count':cart_count,})


def delete_address(request,delete_id):
    address = Address.objects.get(id = delete_id)
    address.is_available = False
    address.save()
    messages.success(request,' Address deleted successfully!')
    
    return redirect('userprofile')

def order_view_user(request,view_id):
    try:
        orderview = Order.objects.get(id=view_id)
        address = Address.objects.get(id=orderview.address.id)
        products = OrderItem.objects.filter(order=view_id)
        variant_ids = [product.variant.id for product in products]
        image = VariantImage.objects.filter(variant__id__in=variant_ids).distinct('variant__color')
        item_status_o=Itemstatus.objects.all()
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
        date = orderview.update_at + timedelta(days=3)

        if date >= timezone.now():
            date = True
        else:
            date = False
        # print(date,'aaaaaaaaaaaaaaaaaaa')   
        
        context = {
            'date' :date,
            'orderview': orderview,
            'address': address,
            'products': products,
            'image' :image,
            'item_status_o' : item_status_o ,
            'wishlist_count':wishlist_count, 
            'cart_count':cart_count,
            
        }   
        return render(request,'userprofile/order_view_user.html',context)

    except Order.DoesNotExist:
        print("Order does not exist")
    except Address.DoesNotExist:
        print("Address does not exist")
    return redirect('userprofile') 

            

