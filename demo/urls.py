# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app = "demo"
urlpatterns = [
    path('create/', views.create, name='create'),
]
