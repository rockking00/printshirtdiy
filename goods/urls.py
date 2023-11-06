# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app = "goods"
urlpatterns = [
    path('', views.home, name='home'),
    path('product/<str:slug>/', views.p_detail, name='p_detail'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('production/<int:pid>/', views.production, name='production'),
    path('export_image/', views.export_image, name='export_image'),
    path('load_more/', views.load_more, name='load_more'),
    path('categories/', views.p_cat, name='p_cat'),
    path('categories/<str:slug>/', views.cat_detail, name='cat_detail'),
]
