from django.shortcuts import render, redirect


def auth(request):
    return render(request, "auth.html")


def sign_in(request):
    try:
        print(f"{request.POST=}")
    except:
        pass
    
    return redirect("home")


def sign_up(request):
    try:
        print(f"{request.POST=}")
    except:
        pass

    return redirect("home")


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def shop(request):
    return render(request, "shop.html")


def product(request):
    return render(request, "shop-single.html")


def cart(request):
    return render(request, "cart.html")


def checkout(request):
    return render(request, "checkout.html")


def contact(request):
    return render(request, "contact.html")


def thank_you(request):
    return render(request, "thankyou.html")