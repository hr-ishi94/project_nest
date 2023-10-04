from django.shortcuts import render,redirect
from .models import *
from django.conf import settings

from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password





import re
import random




def user_signup(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            user=CustomUser.objects.get(email=get_email)
            if not re.search(re.compile(r'^\d{4}$'),get_otp):
                messages.error(request,'OTP should only contain numeric!')
                return render(request,'user/signup.html',{'otp':True,'user':user})
            session_otp=request.session.get('otp')
            if int(get_otp)==session_otp:
                user.is_active=True
                user.save()
                auth.login(request,user)
                messages.success(request,f"Account is created for {user.first_name}")
                if 'otp' in request.session:
                   del request.session['otp']
                return redirect('index')
            else:
                messages.warning(request,'You Entered incorrect otp!')
                return render(request,'user/signup.html',{'otp':True,'user':user})
        else:
            get_otp=request.POST.get('otp1')
            email=request.POST.get('user1')
            if get_otp:
                user=CustomUser.objects.get(email=email)
                messages.error(request,'user/signup.html',{'otp':True,'user':user})
            else:
                firstname=request.POST.get('fname')
                lastname=request.POST.get('lname')
                phonenumber=request.POST.get('phonenumber')    
                email=request.POST.get('email')
                password1=request.POST.get('password1')
                password2=request.POST.get('password2')

                context={
                    'pre_firstname': firstname,
                    'pre_lastname':lastname,
                    'pre_phonenumber':phonenumber,
                    'pre_email':email,
                    'pre_password1':password1,
                    'pre_password2':password2
                }
                if(firstname.strip()=='' or lastname.strip() =='' or email.strip()=='' or phonenumber.strip()==''or password1.strip()=='' or password2.strip()==''):
                    messages.error(request,'Fields cannot be empty!')
                    return render(request,'user/signup.html',context)
                elif CustomUser.objects.filter(phone_number=phonenumber).exists():
                    user=CustomUser.objects.get(phone_number=phonenumber)
                    if user.last_login is None:
                        user.delete()
                    else:
                        messages.error(request,'Phonenumber already exist!')
                        context['pre_phonenumber']=''
                        return render(request,'user/signup.html',context) 
                elif not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),phonenumber):
                    messages.error(request,'phonenumber should only contain numeric!')
                    context['pre_phonenumber']=''
                    return render(request,'user/signup.html',context)
                elif CustomUser.objects.filter(email=email).exists():
                    user=CustomUser.objects.get(email=email)
                    if user.last_login is None:
                        user.delete()
                    else:
                        messages.error(request,'Email already exist!')  
                        context['pre_email']=''
                        return render(request,'user/signup.html',context)
                elif password1 !=password2:
                    messages.error(request,'password does not match')
                    context['pre_password1']=''
                    context['pre_password2']=''
                    return render(request,'user/signup.html',context)
                
                email_check=validateemail(email)
                if email_check is False:
                    messages.error(request,'email not valid!')
                    context['pre_email']=''
                    return render(request,'user/signup.html',context)
                
                password_check=validatepassword(password1)
                if password_check is False:
                    messages.error(request,'Enter a strong password!')
                    context['pre_password1']=''
                    context['pre_password2']=''
                    return render(request,'user/signup.html',context)
                
                phonenumber_checking=len(phonenumber)
                if not phonenumber_checking==10:
                    messages.error(request,'Phone number should contain 10 digits!')
                    context['pre_phonenumber']=''
                    return render(request,'user/signup.html',context)
                if phonenumber=='0000000000':
                    messages.error(request,'Phone number not valid!')
                    context['pre_phonenumber']=''
                    return render(request,'user/signup.html',context)
                
                user=CustomUser.objects.create_user(first_name=firstname,last_name=lastname,email=email,phone_number=phonenumber,username=phonenumber,password=password1)
                user.is_active=False
                user.last_login=None
                user.save()
                user_otp=random.randint(1000,9999)
                request.session['otp']=user_otp
                print(user_otp,'account')
                mess=f'Hello \t{user.first_name},\nYour otp to verify your account for Nest mart and Grocery is {user_otp}\nThankYou!'
                send_mail(
                    "Welcome to Nest e-cart,Please verify your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user.email],

                    fail_silently=False
                    )
                return render(request,'user/signup.html',{'otp':True,'user':user})
    
    return render(request,'user/signup.html')

def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def validatepassword(password1):
    try:
        validate_password(password1)
        return True
    except ValidationError:
        return False 

def user_login1(request):
    
    if request.method=='POST':
        number_mail=request.POST.get('number_mail')
        password=request.POST.get('password')

        if number_mail.strip()=='' or password.strip()=='':
            messages.error(request,'Fields cannot be empty!')
            return redirect('user_login1')
        
        if CustomUser.objects.filter(phone_number=number_mail):
            user=CustomUser.objects.get(phone_number=number_mail)
            username=user.username
        else:
            if CustomUser.objects.filter(email=number_mail):
                user=CustomUser.objects.get(email=number_mail)
                username=user.username
            else:
                messages.error(request,'Enter valid email or phone number!')
                return redirect('user_login1')

            user=authenticate(username=username,password=password)   
            if user is not None:

                if user.is_active:
                    print('hello')
                    login(request,user)
                    return render(request,'core/index.html')
                else:
                    messages.warning(request,'Your account has been blocked!' )
                    return redirect('user_login1')  
            else:
                messages.error(request,'invalid username or password!')
                return redirect('user_login1')    


    return render (request,'user/login.html') 

def user_loginotp(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            user=CustomUser.objects.get(email=get_email)
            if not re.search(re.compile(r'^\d{4}$'), get_otp): 
                messages.error(request,'OTP should only contain numeric!')
                return render(request,'user/loginwithotp.html',{'otp':True,'user':user}) 
            session_otp=request.session.get('otp')
            if int(get_otp) == session_otp:
                auth.login(request,user)
                if 'otp' in request.session:
                   del request.session['otp']
                return redirect('index')   
            else:
                messages.warning(request,'You Entered a wrong OTP!')
                return render(request,'user/loginwithotp.html',{'otp':True,'user':user})
        else:
            get_otp=request.POST.get('otp1')
            email=request.POST.get('user1')
            if get_otp:
                user=CustomUser.objects.get(email=email)
                messages.error(request,'Field cannot be empty!')
                return render(request,'user/loginwithotp.html',{'otp':True,'user':user})
            else:
                email= request.POST['email']

                if email.strip()=='':
                    messages.error(request,'Fields cannot be empty!')
                    return redirect('user_loginotp')
                
                email_check=validateemail(email)
                if email_check is False:
                    messages.error(request,'Enter a valid email!')
                    return render(request,'user/loginwithotp.html')
                
                if CustomUser.objects.filter(email=email):
                    user=CustomUser.objects.get(email=email)
                    user_otp=random.randint(1000,9999)
                    request.session['otp']=user_otp
                    mess=f'Hello \t{user.first_name},\nYour otp to verify your account for Nest mart and Grocery is {user_otp}\nThankYou!'
                    send_mail(
                        "Welcome to Nest e-cart,Please verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [user.email],

                        fail_silently=False
                    )
                    return render(request,'user/loginwithotp.html',{'otp':True,'user':user}) 
                else:
                    messages.error(request,'Email does not exist!')
                    return render(request,'user/loginwithotp.html')
    return render(request,'user/loginwithotp.html')        

@login_required(login_url='user_login1')
def logout1(request):
    logout(request)
    return render(request,'core/index.html')

def forgot_password(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')

        if get_otp:
            get_email=request.POST.get('email')
            user=CustomUser.objects.get(email=get_email)
            if not re.search(re.compile(r'^\d{4}$'), get_otp): 
                messages.error(request,'OTP should only contain numeric!')
                return render(request,'user/password_forgot.html',{'otp':True,'user':user}) 
            session_otp=request.session.get('otp')
            if int(get_otp)==session_otp:
                password1=request.POST.get('password1')
                password2=request.POST.get('password2')
                context={
                    'pre_otp':get_otp,
                }
                if password1.strip()=='' or password2.strip()=='':
                    messages.error(request,'Fields cannot be empty!')
                    return render(request,'user/password_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                elif password1!=password2:
                    messages.error(request,'Passwords doesnot match!')
                    return render(request,'user/password_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                curpass=user.password
                if password1==curpass:
                    messages.error(request,'New password should not match old password')
                    return render(request,'user/password_forgot.html',{'user':user,'otp':True,'pre_otp':get_otp})
                Pass=validatepassword(password1)
                if Pass is False:
                    messages.error(request,'Please enter a strong password!')
                    return render(request,'user/password_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                user.set_password(password1)
                user.save()
                if 'otp' in request.session:
                   del request.session['otp']
                messages.success(request,'Your Password has been changed!')
                return redirect('user_login1')
            else:
                messages.warning(request,'You Entered a wrong OTP!')
                return render(request,'user/password_forgot.html',{'otp':True,'user':user})   

        else:
            get_otp=request.POST.get('otp1')
            email=request.POST.get('user1')
            if get_otp:
                user=CustomUser.objects.get(email=email)
                messages.error(request,'field cannot be empty!')
                return render(request,'user/password_forgot.html',{'otp':True,'user':user}) 
            else:
                email=request.POST['email']

                if email.strip()=='':
                    messages.error(request,'field cannot be empty!')
                    return render(request,'user/password_forgot.html')  
                email_check=validateemail(email)
                if email_check is False:
                    messages.error(request,'email not valid!') 
                    return render(request,'user/password_forgot.html')

                if CustomUser.objects.filter(email=email):
                    user=CustomUser.objects.get(email=email)
                    user_otp=random.randint(1000,9999)
                    request.session['otp']=user_otp
                    mess=f'Hello \t{user.first_name},\nYour otp to verify your account for Nest mart and Grocery is {user_otp}\nThankYou!'
                    send_mail(
                        "Welcome to Nest e-cart,Please verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [user.email],

                        fail_silently=False
                    )
                    return render(request,'user/password_forgot.html',{'otp':True,'user':user})
                else:
                    messages.error(request,'email does not exist!')
                    return render(request,'user/password_forgot.html')
                                
                        

    return render(request,'user/password_forgot.html')
                    


