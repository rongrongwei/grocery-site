import datetime

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.conf import settings


class Product(models.Model):

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50, null=True)
    product_description = models.CharField(max_length=250, null=True)
    product_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    product_price_unit = models.CharField(max_length=50, null=True)
    product_added = models.DateTimeField(auto_now=True, null=True)
    product_img_url = models.CharField(max_length=100, null=True)

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    class Meta:
        db_table = 'product'

class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)









