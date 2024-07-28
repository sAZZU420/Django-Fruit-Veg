from django.db import models
from home.models import Product
from accounts.models import Account


class Cart(models.Model):
    cart_id = models.CharField(max_length=300, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    single_product_code = models.CharField(max_length=200, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def get_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
