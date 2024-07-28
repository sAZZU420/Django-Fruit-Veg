from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderPaymentInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ("user", "payment", "product", "quantity", "product_price", "is_ordered",)
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "email", "order_number", "payment", "status", "created_at", "is_ordered",]
    list_filter = ["user", "email", "order_number", "is_ordered", "status",]
    search_fields = ["user", "email", "order_number", "payment",]
    ordering = ['-created_at',]
    list_per_page = 20
    inlines = [OrderPaymentInline]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "payment_id", "payment_method", "amount_paid", "status",)
    list_filter = ("user", "payment_id", "payment_method", "status",)
    search_fields = ("user", "payment_id",)
    ordering = ('-created_at',)


class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "order", "payment", "product", "quantity", "product_price", "is_ordered",)
    list_filter = ("user", "order", "payment",)
    search_fields = ("user", "order",)
    ordering = ('-created_at',)


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderPaymentAdmin)
