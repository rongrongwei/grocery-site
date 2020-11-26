from django.contrib import admin

from .models import Product

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

admin.site.register(Product, ProductAdmin)
