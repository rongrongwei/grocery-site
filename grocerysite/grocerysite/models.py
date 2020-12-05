from django.db import models
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
# from grocerysite.grocerysite import settings


class Product(models.Model):

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50, null=True)
    product_description = models.CharField(max_length=250, null=True)
    product_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    product_price_unit = models.CharField(max_length=50, null=True)
    product_added = models.DateTimeField(auto_now=True, null=True)
    product_img_url = models.CharField(max_length=100, null=True)
    #NEW**********************************
    slug =models.SlugField(default='test')
    image = models.ImageField(default='test')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })
    #**********************************
    class Meta:
        db_table = 'product'


#NEW******************************************

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
#NEW******************************************
