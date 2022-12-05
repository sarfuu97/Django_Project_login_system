from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Customer_Data
from django.contrib import messages
from django.core import serializers
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import uuid
from .models import *
from testapp.email import *
from django.http import HttpResponse



# Create your views here.
def user_signup(request):
    if request.method=='POST':
        username=request.POST['uname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if pass1 != pass2:
            messages.info(request,'your password not matched')
            return redirect ('user_signup')   
        elif User.objects.filter(username=username).exists():
            messages.info(request,'userName Alredy taken')
            return redirect ('user_signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'email ID already teken')
        else:
            

            obj=Customer_Data()
            obj.username=username
            obj.email=email
            obj.pass1=pass1
            obj.pass2=pass2
            obj.save()
            
            user_obj=User(username=username,email=email)
            user_obj.set_password(pass1)
            user_obj.save()
            email_token=str(uuid.uuid4())
            my_profile=Profile.objects.create(user=user_obj,email_token=email_token)
            my_profile.save()
            send_email_token(email,email_token)
    
            messages.success(request,f'{username} your account created successfully,please verify before login')
            # my_user=User.objects.create_user(username=username,email=email,password=pass1)
            # my_user.save()
            return redirect ('sign_in')
        

    return render(request,'signup.html')


def sign_in(request):
    if request.method=='POST':
        username=request.POST['uname']
        pass1=request.POST['pass1']
        my_ver=User.objects.filter(username=username).first()
        if my_ver is None:
            messages.success(request,'User not found')
            return redirect('sign_in')
        my_prof=Profile.objects.filter(user=my_ver).first()
        if not my_prof.is_verified:
            messages.success(request,'you are not verified please check your email!!!')
            return redirect('sign_in')
        my_auth=authenticate(username=username,password=pass1)
        if my_auth is None:
            messages.success(request,'wrong password ')
            return redirect('sign_in')

        else:      
            login(request,my_auth)
            return redirect('home')



        # my_signin=authenticate(request,username=username,password=pass1)
        # my_signin.save()
        # if my_signin is not None:
        #     login(request,my_signin)
        #     return redirect('home')
        # else:
        #     messages.info(request, 'error')
        #     return redirect('sign_in')
      
    return render(request,'signin.html')

@login_required
def home(request):
    my_data=serializers.serialize('python',Customer_Data.objects.all())
    context={
        'my_data':my_data
    }

    return render(request,'home.html',context)

# for logout 
def log_out (request):
    logout(request)
    return redirect ('sign_in')

# for admin panel access only employee
@login_required(login_url='employee')
def employee (request):

    return render(request, 'employee.html')

def verify(request,token):
    try:
    
        profile_obj=Profile.objects.filter(email_token=token).first()
        if profile_obj.is_verified:
            messages.info(request,'your account is already verified')
            return redirect('sign_in')

        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'hurry!,your has been verrified')
        return redirect ('sign_in')
    

    except Exception as e:
        return HttpResponse('error')
