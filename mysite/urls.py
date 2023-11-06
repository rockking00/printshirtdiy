# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('goods.urls')),
    path('', include('demo.urls')),
    path('', include('cart.urls')),
    path('', include('accounts.urls')),
    path('', include('blog.urls')),
    path('summernote/', include('django_summernote.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
