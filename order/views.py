from django.shortcuts import render, redirect
from django.http import HttpResponse
import uuid
from .models import Order, Payment, OrderProduct
from cart.models import Cart, CartItem
from home.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from accounts.models import Account


@login_required(login_url="/login/")
def order_billing(request, sub_total=0, quantity=0):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        order_note = request.POST.get('order_note')

        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            sub_total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (sub_total * 0.15)
        total = sub_total + (sub_total * 0.15)

        order_number = uuid.uuid4()
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            country=country,
            state=state,
            city=city,
            order_note=order_note,
            order_total=total,
            order_number=order_number,
            tax=tax,
            ip=request.META['REMOTE_ADDR']
        )
        order.save()

        orders = Order.objects.get(user=request.user, order_number=order_number, is_ordered=False)
        context = {
            'order': orders,
            'cart_items': cart_items,
            'sub_total': sub_total,
            'total': total,
            'tax': tax,
            'quantity': quantity
        }
        return render(request, "order/payment_system.html", context)
    else:
        return redirect("store")


def payment_by(request):
    if request.method == "POST":
        payment_way = request.POST.get('buttons')
        order_number = request.POST.get('order_number')
        if payment_way == "cash_on_delivery":
            order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)

            payment = Payment.objects.create(
                user=order.user,
                payment_id=order.order_number,
                payment_method=payment_way,
                amount_paid=payment_way,
                status="DUE"
            )
            payment.save()

            order.is_ordered = True
            order.payment = payment
            order.status = payment.status
            order.save()

            cart_items = CartItem.objects.filter(user=order.user)
            payment = Payment.objects.get(payment_id=order_number)
            for cart_item in cart_items:
                price = (cart_item.product.price * cart_item.quantity)
                order = Order.objects.get(order_number=order_number)
                order_product = OrderProduct.objects.create(
                    user=order.user,
                    order=order,
                    payment=payment,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    product_price=price,
                    is_ordered=True
                )
                order_product.save()

                product = Product.objects.get(product_name=cart_item.product)
                product.in_stocks -= cart_item.quantity
                product.save()

                cart_item.delete()

            messages.success(request, 'order success.Payment Due')
            return redirect("successful_payment", tran_id=order_number, val_id=order_number)

        elif payment_way == "bkash":
            order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)

            store_id = 'djang668e48d222044'
            store_password = "djang668e48d222044@ssl"
            ssl_cz = SSLCOMMERZ({'store_id': store_id, 'store_pass': store_password, 'issandbox': True})
            domain = get_current_site(request).domain
            status_url = f'http://{domain}/ssl_status/'

            data = {
                'total_amount': order.order_total,
                'currency': "BDT",
                'tran_id': order.order_number,
                'success_url': status_url,
                # if transaction is successful, user will be redirected here
                'fail_url': status_url,
                # if transaction is failed, user will be redirected here
                'cancel_url': status_url,
                # after user cancels the transaction, will be redirected here
                'emi_option': "NO",
                'cus_name': f"{order.first_name} {order.last_name}",
                'cus_email': order.email,
                'cus_phone': order.phone_number,
                'cus_add1': order.address_line_1,
                'cus_city': order.city,
                'cus_country': order.country,
                'shipping_method': "NO",
                'multi_card_name': "NO",
                'num_of_item': "NO",
                'product_name': "NO",
                'product_category': "NO",
                'product_profile': "general",
            }
            response = ssl_cz.createSession(data)
            return redirect(response['GatewayPageURL'])
        else:
            return redirect('order_billing')
    return redirect('home')


@csrf_exempt
def ssl_status(request):
    if request.method == "POST":
        payment_data = request.POST
        bank_tran_id = payment_data['bank_tran_id']
        status = payment_data['status']
        if status == "VALID":
            # create payment
            tran_id = payment_data['tran_id']
            order = Order.objects.get(order_number=tran_id)
            amount_paid = payment_data['amount']
            val_id = payment_data['val_id']
            card_type = payment_data['card_type']

            payment = Payment.objects.create(
                user=order.user,
                payment_id=val_id,
                payment_method=card_type,
                amount_paid=amount_paid,
                status=status
            )
            payment.save()

            # create order
            order.is_ordered = True
            order.payment = payment
            order.status = payment.status
            order.save()

            cart_items = CartItem.objects.filter(user=order.user)
            payment = Payment.objects.get(payment_id=val_id)
            for cart_item in cart_items:

                # create order products
                price = (cart_item.product.price * cart_item.quantity)
                order = Order.objects.get(order_number=tran_id)
                order_product = OrderProduct.objects.create(
                    user=order.user,
                    order=order,
                    payment=payment,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    product_price=price,
                    is_ordered=True
                )
                order_product.save()

                # decrease products

                product = Product.objects.get(product_name=cart_item.product)
                product.in_stocks -= cart_item.quantity
                product.save()

                # delete cart items
                cart_item.delete()

            messages.success(request, 'order success.Payment Successfully Done')
            return redirect("successful_payment", tran_id=tran_id, val_id=val_id)
        else:
            return redirect("home")


def successful_payment(request, tran_id, val_id):
    # successful email to user
    try:
        order = Order.objects.get(order_number=tran_id)
        payment = Payment.objects.get(payment_id=val_id)
        mail_sub = "Thanks for Your Order"
        message = render_to_string('order/successful_payment_email.html', {
            'user': request.user,
            'order': order,
            'payment': payment
        })
        email = request.user.email
        send_email = EmailMessage(subject=mail_sub, body=message, to=[email])
        send_email.send()
    except (ValueError, OverflowError, TypeError):
        pass
    order = Order.objects.get(order_number=tran_id)
    order_products = OrderProduct.objects.filter(order=order)
    payment = Payment.objects.get(payment_id=val_id)
    subtotal = order.order_total - order.tax
    context = {
        'order_products': order_products,
        'order': order,
        'payment': payment,
        'subtotal': subtotal
    }
    return render(request, 'order/successful_payment.html', context)


@login_required(login_url="/login/")
def buy_product(request, product_slug, sub_total=0, total=0, tax=0, quantity=0):
    product = Product.objects.get(product_slug=product_slug)
    single_product_code = uuid.uuid4()
    single_cart_item = CartItem.objects.create(
            user=request.user,
            single_product_code=single_product_code,
            product=product,
            quantity=1
        )
    single_cart_item.save()
    try:
        cart_items = CartItem.objects.filter(user=request.user, single_product_code=single_product_code)
        for cart_item in cart_items:
            sub_total = (cart_item.product.price * cart_item.quantity)
            tax = (sub_total * 0.15)
            total = sub_total + (sub_total * 0.15)
            quantity = cart_item.quantity
    except (ValueError, CartItem.DoesNotExist):
        cart_items = None

    context = {
        'cart_items': cart_items,
        'sub_total': sub_total,
        'total': total,
        'tax': tax,
        'quantity': quantity
    }
    urls = ["cart/checkout.html", "order/payment_system.html"]
    for url in urls:
        return render(request, url, context)
