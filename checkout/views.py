import random
import string
from django.shortcuts import redirect, render
from coupon.models import Coupon
from django.db import transaction

from wishlist.models import Wishlist
from .models import Order, OrderItem,OrderAddress
from products.models import Product,Size,Color
from variant.models import Variant,VariantImage
from cart.models import Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from userprofile.models import Address,Wallet
from user.models import CustomUser
from django.contrib import messages

def checkout(request):
    request.session['coupon_session']=0
    request.session['coupon_id']= None
    
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        if coupon is None:
            messages.error(request, 'coupon field is cannot empty!')
            return redirect('checkout')
        try:
            check_coupons =Coupon.objects.filter(coupon_code=coupon).first()
            cartitems = Cart.objects.filter(user=request.user)
    
            total_price = 0
            offer_price = 0
            offer_price_total=0
            all_offer =0
            for item in cartitems:
                if item.variant.product.offer:
                    product_price = item.variant.product.product_price
                    total_price += product_price * item.product_qty
                    offer_price = item.variant.product.offer.discount_amount
                    offer_price_total =offer_price*item.product_qty
                    total_price= total_price - offer_price_total
                    all_offer= all_offer+offer_price_total
                else:     
                    product_price = item.variant.product.product_price
                    total_price += product_price * item.product_qty
                    
           
            grand_total = total_price
            if grand_total>=check_coupons.min_price:
                
                coupon=check_coupons.coupon_discount_amount
                coupon_id=check_coupons.id
                
                request.session['coupon_session']= coupon
                request.session['coupon_id']= coupon_id
                
                
                
                
                messages.success(request, 'This coupon added successfully!')
            else:
                coupon=False 
                messages.error(request, ' purchase minimum price!')    
                
            address = Address.objects.filter(user= request.user,is_available=True)
            cart_count =Cart.objects.filter(user =request.user).count()
            wishlist_count =Wishlist.objects.filter(user=request.user).count()
            coupon_checkout =Coupon.objects.filter(is_available=True)
            if offer_price_total == 0:
                offer_price_total =False
            else:
                offer_price_total

            context = {
                'all_offer':all_offer,
                'offer' :offer_price_total,
                'coupon_checkout':coupon_checkout,
                'cartitems': cartitems,
                'total_price': total_price,
                'grand_total': grand_total,
                'address': address,
                'wishlist_count':wishlist_count,
                'cart_count' :cart_count,   
                'coupon':coupon
                
            }
            if total_price==0:
                return redirect('index')
            else:
                return render(request,'checkout/checkout.html',context)
                
             
                
                
                 
        except:
            messages.error(request, 'This coupon not valid!')
            return redirect('checkout')
    
    cartitems = Cart.objects.filter(user=request.user)
    
    total_price = 0
    offer_price = 0
    offer_price_total=0
    all_offer= 0
    for item in cartitems:
        if item.variant.product.offer:
            product_price = item.variant.product.product_price
            total_price += product_price * item.product_qty
            offer_price = item.variant.product.offer.discount_amount
            offer_price_total =offer_price*item.product_qty
            total_price= total_price - offer_price_total
            all_offer= all_offer+offer_price_total
        else:     
            product_price = item.variant.product.product_price
            total_price += product_price * item.product_qty
    
    
    grand_total = total_price 

    address = Address.objects.filter(user= request.user,is_available=True)
    cart_count =Cart.objects.filter(user =request.user).count()
    wishlist_count =Wishlist.objects.filter(user=request.user).count()
    coupon_checkout =Coupon.objects.filter(is_available=True)
    coupon =False
    if offer_price_total ==0:
        offer_price_total =False
    else:
        offer_price_total

    context = {
        'all_offer':all_offer,
        'offer' :offer_price_total,
        'coupon_checkout':coupon_checkout,
        'cartitems': cartitems,
        'total_price': total_price,
        'grand_total': grand_total,
        'address': address,
        'wishlist_count':wishlist_count,
        'cart_count' :cart_count,  
        'coupon':coupon
        
    }
    if total_price==0:
       return redirect('index')
    else:
           
        return render(request,'checkout/checkout.html',context)




def placeorder(request):
    if request.method == 'POST':
        # Retrieve the current user
        
        user = request.user
        # Retrieve the address ID from the form data
        coupon = request.POST.get('couponOrder')
        address_id = request.POST.get('address')
        if address_id is None:
            messages.error(request, 'Address field is mandatory!')
            return redirect('checkout')

        # Retrieve the selected address from the database
        address = Address.objects.get(id=address_id)

        # Create a new Order instance and set its attributes
        neworder = Order()
        neworder.address=address
        neworder.user = user
        neworder.payment_mode = request.POST.get('payment_method')
        neworder.message = request.POST.get('order_note')
        session_coupon_id=request.session.get('coupon_id')
        if session_coupon_id!=None:
            session_coupons =Coupon.objects.get(id=session_coupon_id)
        else:
            session_coupons = None
               
        neworder.coupon = session_coupons
        

        # Calculate the cart total price 
        cart_items = Cart.objects.filter(user=user)
        cart_total_price = 0
        offer_total_price = 0
        
        for item in cart_items:
            if item.variant.product.offer:
                product_price = item.variant.product.product_price
                cart_total_price += product_price * item.product_qty
                offer_total_price =item.variant.product.offer.discount_amount
                offer_total_price = offer_total_price*item.product_qty
                cart_total_price = cart_total_price - offer_total_price  
                
            else:    
                product_price = item.variant.product.product_price
                cart_total_price += product_price * item.product_qty
        # print(coupon,'asdfghjkjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')    
        
    
        
        
        session_coupon=request.session.get('coupon_session')
        cart_total_price = cart_total_price - session_coupon
        neworder.total_price = cart_total_price

        # Generate a unique tracking number
        track_no = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = random.randint(1111111, 9999999)
        neworder.tracking_no = track_no

        neworder.payment_id = generate_random_payment_id(10)
        while Order.objects.filter(payment_id=neworder.payment_id).exists():
            neworder.payment_id = generate_random_payment_id(10)

        neworder.save()

        OrderAddress.objects.create(
            order=neworder,
            first_name=address.first_name,
            last_name=address.last_name,
            phone=address.phone,
            email=address.email,
            address=address.address,
            country=address.country,
            state=address.state,
            city=address.city,
            pincode=address.pincode,
            order_note=address.order_note,
        )

        # Create OrderItem instances for each cart item
        for item in cart_items:
            OrderItem.objects.create(
                order=neworder,
                variant=item.variant,
                price=item.variant.product.product_price,
                quantity=item.product_qty,
                
            )

            # Decrease the product quantity from the available stock
            product = Variant.objects.filter(id=item.variant.id).first()
            product.quantity -= item.product_qty
            product.save()

        # Delete the cart items after the order is placed 
            cart_items.delete()

        payment_mode = request.POST.get('payment_method')
        if payment_mode == 'cod' or payment_mode == 'razorpay' :
            del request.session['coupon_session']
            del request.session['coupon_id']
            
    
            return JsonResponse({'status': "Your order has been placed successfully"})

        if payment_mode == 'wallet':
            # Check if the wallet balance is sufficient for the order
            wallet = Wallet.objects.get(user=user)
            if wallet.wallet >= neworder.total_price:
                # Deduct the order amount from the wallet balance
                wallet.wallet -= neworder.total_price
                wallet.save()

                # Save the order and related items
                with transaction.atomic():
                    neworder.save()
                    
                    for item in cart_items:
                            OrderItem.objects.create(
                            order=neworder,
                            variant=item.variant,
                            price=item.variant.product.product_price,
                            quantity=item.product_qty,
                
            )
                        # ... (create OrderItem instances and decrease product quantity)

                # Clear the cart and session data
                cart_items.delete()
                del request.session['coupon_session']
                del request.session['coupon_id']

                return JsonResponse({'status': "Your order has been placed successfully"})
            else:
                return JsonResponse({'status': "Your wallet amount is very low"})    
    
        
        
    return redirect('checkout')



def generate_random_payment_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def razarypaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    total_offer = 0
    for item in cart:
        if item.variant.product.offer:
            total_price = total_price + item.variant.product.product_price * item.product_qty
            total_offer = item.variant.product.offer.discount_amount*item.product_qty
            total_price = total_price-total_offer
        else:    
            total_price = total_price + item.variant.product.product_price * item.product_qty
    session_coupon=request.session.get('coupon_session')
    total_price = total_price - session_coupon  
    
      
 
         
    return JsonResponse({'total_price': total_price})


def order_invoice(request,invoice_id):
    order=Order.objects.get(id=invoice_id)
    products=OrderItem.objects.filter(order=invoice_id)
    Variant_id=[product.variant.id for product in products]
    totaloffer=0
    for i in products:
        totaloffer += i.variant.product.offer.discount_amount*i.quantity



    return render(request,'checkout/payment_success.html',{'order':order,'products':products,'total_offer':totaloffer})