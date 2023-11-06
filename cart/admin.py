from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'status', 'user_products', 'notes', 'full_name', 'address', 'address2', 'city', 'state', 'zip_code',
                    'email', 'country', 'created_at', 'total')
    list_per_page = 10
    search_fields = ['email']
    empty_value_display = 'NA'
    list_filter = ('status', 'email',)

admin.site.register(Order, OrderAdmin)

admin.site.site_header = 'UprintMate管理后台'  # 设置header
admin.site.site_title = 'UprintMate管理后台'   # 设置title
admin.site.index_title = 'UprintMate管理后台'
