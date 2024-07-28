from django.urls import path
from . import views

urlpatterns = [
    path('order_billing/', views.order_billing, name="order_billing"),
    path('payment_by/', views.payment_by, name="payment_by"),
    path('payment_by/<slug:product_slug>/', views.buy_product, name="buy"),

    path('ssl_status/', views.ssl_status, name="ssl_status"),
    path('successful_payment/<tran_id>/<val_id>', views.successful_payment, name="successful_payment"),


]
