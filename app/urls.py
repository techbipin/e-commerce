from django.urls import path
from .views import (
    home,
    auth,
    sign_in,
    sign_up,
    sign_out,
    verify_account,
    about,
    shop,
    product,
    cart,
    add_to_cart,
    remove_from_cart,
    checkout,
    contact,
    thank_you
)


urlpatterns = [

    path('', home, name="home"),
    path('auth/', auth, name="auth"),
    path('sign-in/', sign_in, name="sign-in"),
    path('sign-up/', sign_up, name="sign-up"),
    
    path('sign-out/', sign_out, name="sign-out"),
    path('verify-account/<str:token>/', verify_account, name="verify-account"),
    path('about/', about, name="about"),
    path('shop/', shop, name="shop"),
    
    path('product/<int:id>/', product, name="product"),
    path('cart/', cart, name="cart"),
    path('add-to-cart/<int:id>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<int:id>/', remove_from_cart, name="remove-from-cart"),
    path('checkout/', checkout, name="checkout"),

    path('contact/', contact, name="contact"),
    path('thank-you/', thank_you, name="thank-you")

]
