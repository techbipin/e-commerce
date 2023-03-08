from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

import random
import string

from .models import (
    User,
    Product,
    Cart
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
                
                if user.is_verified:
                    login(request, user)
                    
                    messages.success(request, "Logged In !")
                    cart_value = Cart.objects.filter(user=request.user).count()
                    
                    request.session["cart"] = cart_value
                    if redirection:
                        return redirect(redirection)
                    else:
                        return redirect("home")
                else:
                    messages.error(request, "Please activate account !")
                    return redirect('auth')
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

            token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
            
            User.objects.create_user(
                name=name,
                email=email,
                contact=contact,
                password=password,
                verify_token=token
            )
            
            send_mail(
                "Shoppers - Account Verification",
                f"Here is you account verification link : {request.get_host()}/verify-account/{token}",
                settings.EMAIL_HOST_USER,
                [email]
            )
            
            messages.success(request, "Registered Successfully ! Please check your email for Account Verification.")
            return redirect("auth")

        else:
            
            messages.error(request, "Invalid Method !")
            return redirect("auth")
    except:
        pass

    return redirect("home")


def verify_account(request, token):
    try:
        user = User.objects.get(verify_token=token)
        user.is_verified = True
    
        user.verify_token = ""
        user.save()
        
        messages.success(request, "Account verified !")
        
    except User.DoesNotExist:
        messages.error(request, "Request expired !")
    
    return redirect("home")


def sign_out(request):
    try:
        request.session.flush()
        logout(request)
        
        messages.success(request, "Logged Out !")
        return redirect("home")
    except:
        messages.error(request, "Unauthorized !")
        return redirect("auth")


def home(request):
    
    get_products = Product.objects.all()
    
    return render(request, "index.html", {"products": get_products})


def about(request):
    return render(request, "about.html")


def shop(request):
    
    print(f"{request.GET=}")
    collection = request.GET.getlist('collection', '')
    size = request.GET.getlist('size', '')
    
    all_products = Product.objects.all()
    
    if not collection and size:
        products = all_products.filter(size__in=size)
    elif collection and not size:
        products = all_products.filter(collection__in=collection)
    elif collection and size:
        products = all_products.filter(collection__in=collection, size__in=size)
    else:
        products = all_products
    
    men_count = all_products.filter(collection="Men").count()
    women_count = all_products.filter(collection="Women").count()
    children_count = all_products.filter(collection="Children").count()
    
    small_count = all_products.filter(size="Small").count()
    medium_count = all_products.filter(size="Medium").count()
    large_count = all_products.filter(size="Large").count()
    
    paginator = Paginator(products, 10)
    
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    return render(request, "shop.html", {
        "page": page,
        
        "men_check": True if "Men" in collection else False,
        "women_check": True if "Women" in collection else False,
        "children_check": True if "Children" in collection else False,
        
        "small_check": True if "Small" in size else False,
        "medium_check": True if "Medium" in size else False,
        "large_check": True if "Large" in size else False,
        
        "men": men_count,
        "women": women_count,
        "child": children_count,
        
        "small": small_count,
        "medium": medium_count,
        "large": large_count
    })


def product(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        product = None
        
    products = Product.objects.all()

    return render(request, "shop-single.html", {
        "product": product,
        "products": products
    })


@login_required(login_url="auth")
def cart(request):
    try:
        cart_items = Cart.objects.filter(user=request.user)
        collective_amount = [each.price for each in cart_items]
        
        total = sum(collective_amount)
         
        return render(request, "cart.html", {"cart": cart_items, "total": total})
    
    except:
        pass


@login_required(login_url="auth")
def add_to_cart(request, id):
    try:
        quantity = request.GET.get('quantity', 1)
        product = Product.objects.get(id=id)
        user = request.user
        
        cart_item = Cart.objects.filter(
            product=product,
            user=user
        )
        
        if not cart_item:
        
            Cart.objects.create(
                product=product,
                user=user,
                quantity=quantity,
                price=product.price*quantity
            )
            
            cart = request.session.get('cart')
            
            cart += 1
            
            request.session["cart"] = cart
            
        else:
            
            cart_item.update(
                quantity=cart_item[0].quantity+quantity,
                price=(cart_item[0].quantity+quantity)*product.price
            )
        
        
        messages.success(request, "Product added in cart !")
        return redirect("shop")

    except Product.DoesNotExist:
        messages.error(request, "Product is not in SKU !")
        return redirect("home")
    
    
@login_required(login_url="auth")
def remove_from_cart(request, id):
    
    product = Product.objects.get(id=id)
    cart_item = Cart.objects.get(
        product=product,
        user=request.user
    )
    
    cart = request.session["cart"]
    
    cart -= 1
    
    request.session["cart"] = cart
    
    cart_item.delete()
    
    messages.success(request, "Product removed")
    return redirect("cart")


@login_required(login_url="auth")
def checkout(request):
    return render(request, "checkout.html")


@login_required(login_url="auth")
def contact(request):
    return render(request, "contact.html")


@login_required(login_url="auth")
def thank_you(request):
    return render(request, "thankyou.html")