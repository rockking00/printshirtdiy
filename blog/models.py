from django.db import models
from django.utils.text import slugify


# 分类
class BlogCategory(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(default='',blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(BlogCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# 文章
class Articles(models.Model):
    aid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, default='', null=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, null=True)
    content = models.TextField(default='')
    # 日期
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField(upload_to='blog_img/', default='', null=True)
    author = models.CharField(max_length=100, default='Admin', null=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Articles, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
