from django.urls import path
from .views import (
    home,
    auth,
    sign_in,
    sign_up,
    about,
    shop,
    product,
    cart,
    checkout,
    contact,
    thank_you
)


urlpatterns = [

    path('', home, name="home"),
    path('auth/', auth, name="auth"),
    path('sign-in/', sign_in, name="sign-in"),

    path('sign-up/', sign_up, name="sign-up"),
    path('about/', about, name="about"),
    path('shop/', shop, name="shop"),
    
    path('product/', product, name="product"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),

    path('contact/', contact, name="contact"),
    path('thank-you/', thank_you, name="thank-you")

]
