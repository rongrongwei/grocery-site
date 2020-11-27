from django.db import models

from grocerysite.grocerysite import settings


class Product(models.Model):

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50, null=True)
    product_description = models.CharField(max_length=250, null=True)
    product_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    product_price_unit = models.CharField(max_length=50, null=True)
    product_added = models.DateTimeField(auto_now=True, null=True)
    product_img_url = models.CharField(max_length=100, null=True)
    
    class Meta:
        db_table = 'product'

#way of capturing what the user actually owns so we use a manytomanyfield
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

#one order consists of many order items
class OrderItem(models.Model):
    Product = models.OneToOneField(Product, on_delete=models.SET_NULL, null =True)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(null=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name

class Order(models.Model):
    ref_code=models.CharField(max_length=15)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])








