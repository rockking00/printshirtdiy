# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views


app = "cart"
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove/', views.remove, name='remove'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('edit/<str:cid><str:pid>/', views.edit_cart_product, name='edit_cart_product'),
]
