from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django_ratelimit.decorators import ratelimit
from django.conf import settings
from django.http import JsonResponse
from .models import Order
from goods.models import UserProducts, CartProducts, Category, ShippingFee, Products
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def cart(request):
    user = request.user
    goods_items = CartProducts.objects.filter(user=user)
    categories = Category.objects.all()
    content = {
        'goods': goods_items,
        'categories': categories,
    }

    return render(request, 'cart/cart.html', content)

# 编辑产品
def edit_cart_product(request, cid, pid):
    cart_product = get_object_or_404(CartProducts, cid=cid)
    products = get_object_or_404(Products, id=pid)
    categories = Category.objects.all()
    front_printdir = products.printdir_set.get(printdir_id="front")
    back_printdir = products.printdir_set.get(printdir_id="back")
    front_image = front_printdir.printdir_moldfile1
    back_image = back_printdir.printdir_moldfile1
    content = {
        'cart_product': cart_product,
        'products': products,
        'categories': categories,
        'cid': cid,
        'pid': pid,
        'front_image': front_image,
        'back_image': back_image,
    }
    if request.method == 'POST':
        num = request.POST.get('num')
        price = request.POST.get('price')
        image_name = request.POST.get('image_name')
        style = request.POST.get('style').split('-')
        color = request.POST.get('color').split('-')
        cart_product.product_id = pid
        cart_product.user = request.user
        cart_product.price = price
        cart_product.style = style[0]
        cart_product.size = request.POST.get('size')
        cart_product.color = color[0]
        cart_product.img_size = request.POST.get('image_size')
        cart_product.num = num
        cart_product.subtotal = int(num) * int(price)
        cart_product.imagename = image_name
        cart_product.left_coordinate = request.POST.get('left_coordinate')
        cart_product.scaling = request.POST.get('scaling')
        cart_product.coicp = request.POST.get('coordinate_of_image_center_point')
        cart_product.upload_name = request.POST.get('upload_name')
        cart_product.save()

        user_product = UserProducts.objects.get(user=request.user, product_id=pid)
        user_product.product_id = pid
        user_product.user = request.user
        user_product.price = price
        user_product.style = style[0]
        user_product.size = request.POST.get('size')
        user_product.color = color[0]
        user_product.img_size = request.POST.get('image_size')
        user_product.num = num
        user_product.subtotal = int(num) * int(price)
        user_product.imagename = image_name
        user_product.left_coordinate = request.POST.get('left_coordinate')
        user_product.scaling = request.POST.get('scaling')
        user_product.coicp = request.POST.get('coordinate_of_image_center_point')
        user_product.save()

    return render(request, 'cart/edit.html', content)

from django.db.models import Sum
def get_cart_count(request):
    if request.user.is_authenticated:
        count = CartProducts.objects.filter(user=request.user).aggregate(Sum('num'))['num__sum'] or 0
    else:
        count = 0
    return JsonResponse({'count': count})

from django.utils.crypto import get_random_string
@login_required
def checkout(request):
    user = request.user
    goods_items = CartProducts.objects.filter(user=user)

    if request.method == 'POST':
        order_number = request.POST['invoice']
        full_name = request.POST['full_name']
        address = request.POST['address']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        email = request.POST['email']
        country = request.POST['country']
        total = request.POST['amount']
        total = str(total).replace('.00', '')
        # 获取购物车中的产品信息
        user_products = UserProducts.objects.filter(user=user)
        notes = request.POST['notes']

        for prod in user_products:
            Order.objects.create(full_name=full_name, address=address, address2=address2,
                                 city=city, state=state, zip_code=zip_code, email=email,
                                 country=country, order_number=order_number, total=total, user_products=prod,
                                 notes=notes)

    # 订单号
    order_number = get_random_string(length=12)
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "item_name": "Products",
        "invoice": f"{order_number}",
        # 处理订单状态
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('payment_success')),
        "cancel_return": request.build_absolute_uri(reverse('cart')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    categories = Category.objects.all()
    shippingfee = ShippingFee.objects.all()
    content = {
        'form': form,
        'order_number': order_number,
        'goods': goods_items,
        'categories': categories,
        'shippingfee': shippingfee,
    }

    return render(request, 'cart/checkout.html', content)

#处理订单状态
@csrf_exempt
def payment_success(request):
    user = request.user
    CartProducts.objects.filter(user=user).delete()
    return render(request, 'cart/payment_done.html')

# 删除产品
def remove(request):
    pid = request.GET.get('id','')
    if pid:
        product = CartProducts.objects.get(cid=pid)
        product.delete()
    prev_url = request.META['HTTP_REFERER']

    return redirect(prev_url)
