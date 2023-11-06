from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# 分类
class Category(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(default='',blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, null=True)
    image = models.ImageField(upload_to='p_category_img/', null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# 运费表
class ShippingFee(models.Model):
    # 费用
    cost = models.DecimalField(max_digits=7, decimal_places=2)
    # 首重
    first_weight = models.DecimalField(max_digits=5, decimal_places=2)
    # 续重
    continuation_weight = models.DecimalField(max_digits=5, decimal_places=2)
    # 物流商
    express = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.express

# 产品
class Products(models.Model):
    isdownnum = (
        ("1",1),
        ("0",0),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default='', null=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, null=True)
    item = models.CharField(max_length=100, default='', null=True)
    intro = models.TextField(default='', null=True)
    description = models.TextField(default='', null=True)
    price = models.IntegerField(default=0, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    isdown = models.CharField(max_length=10, default='0', choices=isdownnum, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# StyleAttribute模型
class StyleAttribute(models.Model):
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_template/', default=None)

    def __str__(self):
        return self.attribute_name

# ColorAttribute模型
class ColorAttribute(models.Model):
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_template/', default=None)

    def __str__(self):
        return self.attribute_name


# 位置模型
class Printdir(models.Model):
    is_defaults = (
        ("1","设置为主图"),
        ("0","否"),
    )
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    printdir_styleid = models.ForeignKey(StyleAttribute,on_delete=models.CASCADE)
    printdir_colorid = models.ForeignKey(ColorAttribute,on_delete=models.CASCADE)
    printdir_id = models.CharField(max_length=100)
    printdir_name = models.CharField(max_length=200)
    printdir_moldfile1 = models.ImageField(upload_to='product_moldfile/')
    is_default = models.CharField(max_length=10, default='0', choices=is_defaults, null=True)
    def __str__(self):
        return self.printdir_name

# SiteAttribute模型
class SiteAttribute(models.Model):
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=100)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.attribute_name

# 产品多图模型
class Image(models.Model):
    imgs = models.ImageField(upload_to='p_image/', default=None)

    shirt = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name='images'
    )


# 用户定制产品信息，用于购物车展示
class UserProducts(models.Model):
    product_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    style = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    # 定制图片占边框的尺寸
    img_size = models.CharField(max_length=255)
    # 数量
    num = models.IntegerField(default=1)
    # 小计
    subtotal = models.IntegerField(default=0)
    imagename = models.CharField(max_length=100, default='')
    left_coordinate = models.CharField(max_length=50, null=True)
    scaling = models.CharField(max_length=50, null=True)
    # 图片中心点坐标
    coicp = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'产品ID:{self.product_id}'

class CartProducts(models.Model):
    cid = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(default=0, null=True)
    style = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True)
    # 定制图片占边框的尺寸
    img_size = models.CharField(max_length=255, null=True)
    # 数量
    num = models.IntegerField(default=1, null=True)
    # 小计
    subtotal = models.IntegerField(default=0, null=True)
    imagename = models.CharField(max_length=100, default='', null=True)
    left_coordinate = models.CharField(max_length=50, null=True)
    scaling = models.CharField(max_length=50, null=True)
    # 图片中心点坐标
    coicp = models.CharField(max_length=50, null=True)
    upload_name = models.CharField(max_length=100, default='', null=True)

    def __str__(self):
        return f'产品ID:{self.cid}'

# 购物车合成图
class ImageFilename(models.Model):
    filename = models.CharField(max_length=200, null=True)
    upload_imgname = models.CharField(max_length=200, null=True)
