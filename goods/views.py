from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Category, Products, UserProducts, CartProducts, ImageFilename
import os, base64, random, string
from cart.models import Order


@ratelimit(key='ip', rate='100/m', block=True)
def home(request):
    products = Products.objects.select_related('category').all()[:9]
    categories = Category.objects.all()
    content = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'goods/index.html', content)

# 分类页
def p_cat(request):
    categories = Category.objects.all()
    content = {
        'categories': categories,
    }
    return render(request, 'goods/cat.html',content)

# 类目详情
def cat_detail(request, slug):
    # 获取slug参数
    cat_ = get_object_or_404(Category, slug=slug)
    pages = cat_.products_set.all()[:9]
    categories = Category.objects.all()
    context = {
        'cat_': cat_,
        'pages': pages,
        'categories': categories,
    }
    return render(request, 'goods/cat_detail.html', context)

# 产品详情
def p_detail(request, slug):
    # 获取slug参数
    product = get_object_or_404(Products, slug=slug)
    category = product.category
    # 相关推荐
    related = Products.objects.filter(category=category).exclude(pk=product.pk)[:8]
    categories = Category.objects.all()
    context = {
        'product': product,
        'category': category,
        'related': related,
        'categories': categories,
    }
    return render(request, 'goods/p_detail.html', context)


@ratelimit(key='ip', rate='100/m', block=True)
def production(request, pid):
    products = get_object_or_404(Products, id=pid)
    categories = Category.objects.all()
    # 正面
    front_printdir = products.printdir_set.get(printdir_id="front")
    # 反面
    back_printdir = products.printdir_set.get(printdir_id="back")
    # 正面图
    front_image = front_printdir.printdir_moldfile1
    # 反面图
    back_image = back_printdir.printdir_moldfile1
    content = {
        'pid': pid,
        'products': products,
        'categories': categories,
        'front_image': front_image,
        'back_image': back_image,
    }

    if request.method == 'POST':
        user = request.user
        price = request.POST.get('price')
        style = request.POST.get('style').split('-')
        size = request.POST.get('size')
        color = request.POST.get('color').split('-')
        img_size = request.POST.get('image_size')
        num = request.POST.get('num')
        subtotal = int(num) * int(price)
        image_name = request.POST.get('image_name')
        upload_name = request.POST.get('upload_name')
        left_coordinate = request.POST.get('left_coordinate')
        scaling = request.POST.get('scaling')
        coicp = request.POST.get('coordinate_of_image_center_point')

        UserProducts.objects.create(user=user,price=price,style=style[0],size=size,color=color[0],img_size=img_size,
                               num=num, subtotal=subtotal,imagename=image_name,left_coordinate=left_coordinate,
                                    scaling=scaling,coicp=coicp)
        CartProducts.objects.create(product_id=pid,user=user, price=price, style=style[0], size=size, color=color[0], img_size=img_size,
                                    num=num, subtotal=subtotal, imagename=image_name,left_coordinate=left_coordinate,
                                    scaling=scaling,coicp=coicp,upload_name=upload_name)

    return render(request, 'goods/productions.html', content)


from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
@csrf_exempt
def upload_image(request):
    image_data = request.FILES['image'].read()
    if image_data:
        # 生成文件名
        filename = 'upload_images/' + ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.jpg'
        # 写入文件
        storage.save(filename, ContentFile(image_data))
        image_url = '/media/' + filename
        return JsonResponse({'image_url': image_url, 'image_name': filename})
    return JsonResponse({'error': 'Upload failed'}, status=400)

@csrf_exempt
def export_image(request):
    image_data = request.POST.get('image_data')
    if image_data:
        image_data = base64.b64decode(image_data.split(',')[1])
        # 生成文件名
        filename = 'synthesis_images/' + ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.jpg'
        ImageFilename.objects.create(filename=filename)
        # 写入文件
        storage.save(filename, ContentFile(image_data))
        return HttpResponse(filename)
    return HttpResponseBadRequest('Upload failed')

# ajax加载
def load_more(request):
    num_items = request.GET.get('num_items', 9)
    loaded_count = request.GET.get('loaded_count')
    products = Products.objects.select_related('category').all()[int(loaded_count):int(loaded_count)+int(num_items)]
    data = []
    for p in products:
        data.append({
            't_id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'image': p.images.first,
        })
    return JsonResponse({'data': data})
