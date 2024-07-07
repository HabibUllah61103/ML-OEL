from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

# from .models import Electronics, Garments, Groceries, Products, Shoppingcarts, Customers, Cartcontainers, Orders
from django.contrib.auth import authenticate, login, logout
from .forms import SigninForm, SignupForm, MainForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import connection
from .models import Customers, History

import pickle

# Load the model from disk
filepath = "./StockEzyApp/Linear Regression.pkl"
with open(filepath, "rb") as file:
    loaded_model = pickle.load(file)


def dashboad_view(request, customer_id):
    if request.method == "POST":
        form = MainForm(request.POST)
        open = float(request.POST.get("open"))
        high = float(request.POST.get("high"))
        low = float(request.POST.get("low"))
        volume = float(request.POST.get("volume"))
        close = loaded_model.predict([[open, high, low, volume]])[0]
        print(close)
        history = History.objects.create(
            custid=Customers.objects.get(custid=customer_id),
            open=open,
            high=high,
            low=low,
            volume=volume,
            close=close,
        )

    else:
        form = MainForm()
        close = 0

    context = {"form": form, "close": close, "id": customer_id}
    return render(request, "dashboard.html", context=context)


def customer_profile(request, customer_id):
    customer = Customers.objects.get(custid=customer_id)
    context = {"customer": customer, "id": customer_id}
    return render(request, "profile.html", context)


def history_view(request, customer_id):
    customer = Customers.objects.get(custid=customer_id)
    customers_history = History.objects.all()
    history = []
    for i in customers_history:
        if i.custid.custid == customer_id:
            history.append(i)

    context = {"history": history, "id": customer_id, "customer": customer}
    return render(request, "tables.html", context)


def customer_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            cpassword = form.cleaned_data["cpassword"]
            cre_password = form.cleaned_data["cre_password"]
            print(cpassword)
            print(cre_password)

            form.save()
            return redirect("customer_signin")
    else:
        form = SignupForm()
    context = {"form": form}
    return render(request, "sign-up.html", context=context)


def customer_signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            cemail = form.cleaned_data["cemail"]
            cpassword = form.cleaned_data["cpassword"]
            user = authenticated(request, cemail=cemail, cpassword=cpassword)
            if user is not None:
                login(request, user)
                customer_id = request.user.custid
                return redirect("dashboard_view", customer_id=customer_id)
            else:
                form.add_error(None, "Invalid email or password")
                return render(request, "sign-in.html", {"form": form})
    else:
        form = SigninForm()
    return render(request, "sign-in.html", {"form": form})


def authenticated(request, cemail=None, cpassword=None, **kwargs):
    try:
        user = Customers.objects.get(cemail=cemail, cpassword=cpassword)
    except Customers.DoesNotExist:
        return None
    else:
        return user
