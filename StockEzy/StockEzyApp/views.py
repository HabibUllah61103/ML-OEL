from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
#from .models import Electronics, Garments, Groceries, Products, Shoppingcarts, Customers, Cartcontainers, Orders
from django.contrib.auth import authenticate, login, logout
from .forms import SigninForm, SignupForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import connection
from .models import Customers


def dashboad_view(request, customer_id):
    return HttpResponse("Hello, world. You're at the StockEzy index.")

def customer_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            cpassword = form.cleaned_data['cpassword']
            cre_password = form.cleaned_data['cre_password']
            print(cpassword)
            print(cre_password)
            
            form.save()
            return redirect('customer_signin')
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'sign-up.html', context=context)

def customer_signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            cemail = form.cleaned_data['cemail']
            cpassword = form.cleaned_data['cpassword']
            user = authenticated(request, cemail=cemail, cpassword=cpassword)
            if user is not None:
                login(request, user)
                customer_id= request.user.custid
                return redirect('dashboard_view', customer_id=customer_id)           
            else:
                form.add_error(None, 'Invalid email or password')
                return render(request, 'sign-in.html', {'form': form})
    else:
        form = SigninForm()
    return render(request, 'sign-in.html', {'form': form})


def authenticated(request, cemail=None, cpassword=None, **kwargs):
        try:
            user = Customers.objects.get(cemail=cemail,  cpassword=cpassword)
        except Customers.DoesNotExist:
            return None
        else:
            return user