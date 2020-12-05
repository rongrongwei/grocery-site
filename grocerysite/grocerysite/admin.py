from django.contrib import admin

from .models import Product, OrderItem, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_id",
        "product_name",
        "product_description",
        "product_price",
        "product_price_unit",
        "product_added",
        "product_img_url",
    )
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]

    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   ]
    search_fields = [
        'user__username',
        'ref_code'
    ]

admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
