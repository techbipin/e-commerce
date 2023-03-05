from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings

from .models import (
    User,
    Product
)


def auth(request):
    return render(request, "auth.html")


def sign_in(request):
    try:

        if request.method == "POST":

            redirection = request.POST.get("next", "home")
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if redirection:
                    return redirect(redirection)
                else:
                    return redirect("home")
            else:
                messages.error(request, "Invalid Credentials !")
                return redirect('auth')
            
        else:
            
            messages.error(request, "Invalid Method !")
            return redirect("auth")
    except:
        return redirect("auth")


def sign_up(request):
    try:
        if request.method == "POST":

            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            contact = request.POST.get('contact', '')
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm-password', '')
            
            if password != confirm_password:
                messages.error(request, "Passwords Does Not Match !")
                return redirect("auth")

            User.objects.create_user(
                name=name,
                email=email,
                contact=contact,
                password=password
            )
            
            messages.success(request, "Registered Successfully ! Please check your email for Account Verification.")
            return redirect("auth")

        else:
            
            messages.error(request, "Invalid Method !")
            return redirect("auth")
    except:
        pass

    return redirect("home")


def sign_out(request):
    logout(request)
    return redirect("home")


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def shop(request):
    
    products = Product.objects.all()
    paginator = Paginator(products, 10)
    
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    return render(request, "shop.html", {
        "page": page
    })


def product(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        product = None

    return render(request, "shop-single.html", {
        "product": product
    })


@login_required(login_url="auth")
def cart(request):
    return render(request, "cart.html")


@login_required(login_url="auth")
def checkout(request):
    return render(request, "checkout.html")


@login_required(login_url="auth")
def contact(request):
    return render(request, "contact.html")


@login_required(login_url="auth")
def thank_you(request):
    return render(request, "thankyou.html")