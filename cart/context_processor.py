from .models import Cart, CartItem, Product
from .views import _cart_id


def content(request):
    if 'admin' in request.path:
        return {}
    else:
        cart_count = 0
        try:

            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart__cart_id=_cart_id(request))

            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
        return dict(cart_count=cart_count)
