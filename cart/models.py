from django.db import models


# 订单
class Order(models.Model):
    # 订单编号
    order_number = models.CharField(max_length=255, editable=False)
    # 状态
    status_ = (
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('S', 'Shipped'),
        ('X', 'Refunded'),
    )
    # 用户名
    full_name = models.CharField(max_length=255)
    # 地址
    address = models.CharField(max_length=255)
    # 地址2
    address2 = models.CharField(max_length=255, blank=True, null=True)
    # 城市
    city = models.CharField(max_length=255)
    # 省
    state = models.CharField(max_length=255)
    # 邮编
    zip_code = models.CharField(max_length=255)
    # 邮箱
    email = models.EmailField(max_length=255)
    # 国家
    country = models.CharField(max_length=255)
    # 日期
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=status_, default='P')
    total = models.IntegerField(default=0)
    user_products = models.ForeignKey('goods.UserProducts', on_delete=models.CASCADE, null=True)
    notes = models.CharField(max_length=255, default='')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.order_number}'

    def update_status(self, new_status):
        """
        更新订单状态
        """
        self.status = new_status
        self.save()
