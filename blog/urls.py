# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views


app = "blog"
urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('blog/<str:slug>/', views.p_detail, name='p_detail'),
    path('c/<str:slug>/', views.cat_detail, name='cat_detail'),
]
