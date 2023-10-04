from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from user.models import *
from django.db.models import Q

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


# @login_required(login_url='admin_login1')
def dashboard(request):
    return render(request,'adminNest/dashboard.html')

# @login_required(login_url='admin_login1')
def usermanagement_1(request):
    users = CustomUser.objects.all().order_by('id')
    return render(request,'adminNest/usermanagement.html',{'users':users})


# @login_required(login_url='admin_login1')   
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

# @login_required(login_url='admin_login1')
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

# @login_required(login_url='admin_login1')
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
    
# @login_required(login_url='admin_login1')
def admin_logout1(request):
    logout(request)
    return redirect('admin_login1')    