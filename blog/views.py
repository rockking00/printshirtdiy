from django.shortcuts import render, get_object_or_404
from .models import Articles, BlogCategory
from goods.models import Category


def blog(request):
    blog_content = Articles.objects.select_related('category').all()[:12]
    categories = Category.objects.all()
    content = {
        'categories': categories,
        'blog_content': blog_content,
    }

    return render(request, 'blog/blog.html', content)


#类目详情页
def cat_detail(request, slug):
    # 获取id参数
    cat_ = get_object_or_404(BlogCategory, name=slug)
    pages = cat_.articles_set.all()[:12]
    categories = Category.objects.all()
    content = {
        'categories': categories,
        'pages': pages
    }
    return render(request, 'blog/cat_detail.html', content)

# 详情页
def p_detail(request, slug):
    # 获取id参数
    articles = get_object_or_404(Articles, slug=slug)
    category = articles.category
    # 相关推荐
    related = Articles.objects.filter(category=category).exclude(pk=articles.pk)[:8]
    categories = Category.objects.all()
    content = {
        'categories': categories,
        'articles': articles,
        'category': category,
        'related': related,
    }
    return render(request, 'blog/p_detail.html', content)

