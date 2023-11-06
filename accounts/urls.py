# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app = "accounts"
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
