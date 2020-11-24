from django.db import models

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
