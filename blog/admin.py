from django.contrib import admin
from .models import Articles, BlogCategory
from django_summernote.admin import SummernoteModelAdmin


class CatAdmin(SummernoteModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name', 'description')
    list_editable = ('name',)
    list_per_page = 10
    search_fields = ['name']
    empty_value_display = 'NA'
    summernote_fields = ('description',)

class ArticleAdmin(SummernoteModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'created_at', 'author', 'category')
    list_per_page = 10
    search_fields = ['title']
    empty_value_display = 'NA'
    list_display_links = ('title',)
    summernote_fields = ('content',)

admin.site.register(BlogCategory, CatAdmin)
admin.site.register(Articles, ArticleAdmin)