from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name="cart"),
    path('cart/<slug:product_slug>', views.add_item, name="add_cart"),
    path('remove_cart/<slug:product_slug>', views.remove_cart, name="remove_cart"),
    path('delete_cart/<slug:product_slug>', views.delete_cart, name="delete_cart"),
    path('cart/checkout/', views.checkout, name="checkout"),
]
