from django.db import models
from accounts.models import Account
from home.models import Product


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = {
        ("NEW", "NEW"),
        ("ACCEPTED", "ACCEPTED"),
        ("COMPLETED", "COMPLETED"),
        ("CANCELLED", "CANCELLED"),
        ("DUE", "DUE"),
        ("VALID", "VALID"),
    }
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=50, null=True, blank=True)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    address_line_1 = models.CharField(max_length=350)
    address_line_2 = models.CharField(max_length=350, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.TextField(max_length=50, blank=True, null=True)
    order_total = models.FloatField()
    tax = models.FloatField()

    status = models.CharField(max_length=50, choices=STATUS, default="NEW")
    ip = models.CharField(blank=True, max_length=50)

    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __iter__(self):
        return self.order_number

    def address(self):
        return self.address_line_1, self.city, self.country


class OrderProduct(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    product_price = models.FloatField()

    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return self.quantity * self.product_price

    def __unicode__(self):
        return self.product
