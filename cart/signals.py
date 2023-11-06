# -*- coding: utf-8 -*-
from paypal.standard.models import ST_PP_COMPLETED, ST_PP_REFUNDED
from paypal.standard.ipn.signals import valid_ipn_received
from .models import Order


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    order_id = ''.join(ipn_obj.invoice)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = Order.objects.filter(order_number=order_id)
        for item in order:
            item.update_status('C')
    elif ipn_obj.payment_status == ST_PP_REFUNDED:
        # 处理退款
        order = Order.objects.filter(order_number=order_id)
        for item in order:
            item.update_status('X')
    else:
        # 处理其它
        order = Order.objects.filter(order_number=order_id)
        for item in order:
            item.update_status('S')

valid_ipn_received.connect(payment_notification)
