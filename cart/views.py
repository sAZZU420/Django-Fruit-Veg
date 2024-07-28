from django.shortcuts import render, redirect
from home.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_item(request, product_slug):
    product = Product.objects.get(product_slug=product_slug)

    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, user=request.user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:

            cart_item = CartItem.objects.create(
                    user=request.user,
                    product=product,
                    quantity=1
                )
            cart_item.save()
        return redirect('cart')

    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request),
            )
            cart.save()

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1
            )
            cart_item.save()
    return redirect('cart')


def remove_cart(request, product_slug):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product__product_slug=product_slug, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product__product_slug=product_slug, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def delete_cart(request, product_slug):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product__product_slug=product_slug, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product__product_slug=product_slug, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, all_total=0,  tax=0, sub_total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart_id = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart_id)
        for cart_item in cart_items:
            sub_total += (cart_item.product.price * cart_item.quantity)
            quantity = quantity + cart_item.quantity
        tax = (sub_total * 0.15)
        all_total = sub_total + (sub_total * 0.15)
    except:
        pass

    context = {
        'cart_items': cart_items,
        'sub_total': sub_total,
        'all_total': all_total,
        'tax': tax,
        'quantity': quantity
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url="/login/")
def checkout(request, total=0,  tax=0, sub_total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart_id = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart_id)
        for cart_item in cart_items:
            sub_total += (cart_item.product.price * cart_item.quantity)
            tax = (sub_total * 0.15)
            total = sub_total + (sub_total * 0.15)
            quantity = quantity + cart_item.quantity
    except (ValueError, CartItem.DoesNotExist):
        cart_items = None

    context = {
        'cart_items': cart_items,
        'sub_total': sub_total,
        'total': total,
        'tax': tax,
        'quantity': quantity
    }
    return render(request, 'cart/checkout.html', context)
