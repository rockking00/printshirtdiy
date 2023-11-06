from django.contrib import admin
from .models import Products, UserProducts, Category, Image, ShippingFee,StyleAttribute,SiteAttribute,ColorAttribute, Printdir
from django.utils.html import format_html
from django.db import models
from django_summernote.admin import SummernoteModelAdmin


class Cat(SummernoteModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name', 'description')
    list_editable = ('name',)
    list_per_page = 10
    search_fields = ['name']
    empty_value_display = 'NA'
    summernote_fields = ('description',)

class ImageAdmin(admin.TabularInline):
    model = Image
    can_delete = True
    extra = 4
    max_num = 6


class SiteAdmin(admin.TabularInline):
    model = SiteAttribute
    can_delete = True
    extra = 1
    max_num = 5

class PrintdirAdmin(admin.TabularInline):
    model = Printdir
    can_delete = True
    extra = 1
    max_num = 5

class CustomProduct(SummernoteModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'price', 'category')
    list_editable = ('price',)
    list_per_page = 10
    search_fields = ['name']
    empty_value_display = 'NA'
    list_display_links = ('name',)
    summernote_fields = ('description', 'intro')
    inlines = [ImageAdmin,SiteAdmin, PrintdirAdmin]


class UserProduct(admin.ModelAdmin):
    list_display = ('product_id', 'user', 'price', 'style', 'size', 'color', 'img_size', 'num', 'show_image')
    list_per_page = 10
    search_fields = ['product_id','user']
    empty_value_display = 'NA'
    def show_image(self, obj):
        return format_html(f'<img src="/media/{obj.imagename}" width="50" height="50"/>')

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('express', 'first_weight', 'continuation_weight', 'cost')
    list_per_page = 10
    search_fields = ['express']
    empty_value_display = 'NA'

class StyleAdmin(admin.ModelAdmin):
    list_display = ('attribute_name', 'attribute_value', 'image')
    list_per_page = 10
    search_fields = ['attribute_name']
    empty_value_display = 'NA'

class ColorAdmin(admin.ModelAdmin):
    list_display = ('attribute_name', 'attribute_value', 'image')
    list_per_page = 10
    search_fields = ['attribute_name']
    empty_value_display = 'NA'


admin.site.register(Products, CustomProduct)
admin.site.register(UserProducts, UserProduct)
admin.site.register(Category, Cat)
admin.site.register(ShippingFee, ShippingAdmin)
admin.site.register(StyleAttribute, StyleAdmin)
admin.site.register(ColorAttribute, ColorAdmin)
