from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .form import RegistrationForm
from .models import Account, UserProfile
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from cart.models import Cart, CartItem
from cart.views import _cart_id

from order.models import OrderProduct, Order, Payment

import requests


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password
                )
            user.phone_number = phone_number
            user.save()

            domain = get_current_site(request)
            mail_sub = "Please Click the link to active Your Account"
            message = render_to_string('account/account_verification.html', {
                'user': user,
                'domain': domain,
                'uuid64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_email = EmailMessage(subject=mail_sub, body=message, to=[email])
            send_email.send()
            return redirect("/login/?command=verification&email="+email)
    else:
        form = RegistrationForm()
    context = {
         'form': form
    }
    return render(request, 'account/registration.html', context)


def activate(request, uuid64, token):
    try:
        uuid64 = urlsafe_base64_decode(uuid64).decode()
        user = Account._default_manager.get(pk=uuid64)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is now activate to use')
        return redirect('login')
    else:
        messages.error(request, 'Account activation fail')
        return redirect('registration')


def log_in(request):
    if request.method == 'POST':
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items_exists = CartItem.objects.filter(cart=cart).exists()

                if cart_items_exists:

                    user_items = []
                    user_item = CartItem.objects.filter(user=user)
                    for item in user_item:
                        user_items.append(item.product)

                    cart_items = CartItem.objects.filter(cart=cart)
                    for cart_item in cart_items:
                        if cart_item.product in user_items:
                            cart_user = CartItem.objects.get(user=user, product=cart_item.product)
                            cart_user.quantity += cart_item
                            cart_user.save()
                        else:
                            cart_item.user = user
                            cart_item.save()

            except (TypeError, ValueError, OverflowError, Cart.DoesNotExist):
                pass

            login(request, user)

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split("&"))
                if "next" in params:
                    next_page = params['next']
                    messages.success(request, 'successfully login')
                    return redirect(next_page)
            except (TypeError, ValueError, OverflowError):
                messages.success(request, 'welcome to your dashboard')
                return redirect('dashboard')
        else:
            messages.error(request, 'username or password')
            return redirect('login')
    return render(request, 'account/login.html')


@login_required(login_url="/login/")
def log_out(request):
    logout(request)
    messages.success(request, 'You are logout')
    return redirect('login')


def forgot_password(request):
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            user = Account.objects.filter(email=email).exists()
            if user is not None:
                user = Account.objects.get(email__iexact=email)
                domain = get_current_site(request)
                mail_sub = "Please Click the link to reset your forgot password"
                message = render_to_string('account/email_verification.html', {
                    'user': user,
                    'domain': domain,
                    'uuid64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_email = EmailMessage(subject=mail_sub, body=message, to=[email])
                send_email.send()
                messages.success(request, 'we sand a email for forget password.check your email for reset password ')
                return redirect('forgot_password')
            else:
                messages.error(request, 'user not found')
                return redirect('forgot_password')
    except Account.DoesNotExist:
        messages.error(request, 'user not found')
        return redirect('forgot_password')
    return render(request, 'account/forgot_password.html')


def email_verification(request, uuid64, token):
    try:
        uuid64 = urlsafe_base64_decode(uuid64).decode()
        user = Account._default_manager.get(pk=uuid64)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uuid64'] = uuid64
        messages.success(request, 'Reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'this link is expire')
        return redirect('forget_password')


def reset_password(request):
    try:
        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                messages.error(request, 'confirm Password not match')
                return redirect('reset_password')
            else:
                uuid64 = request.session.get('uuid64')
                user = Account.objects.get(pk=uuid64)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successfully')
                return redirect('login')
    except (ValueError, TypeError, ValueError, OverflowError):
        messages.error(request, 'give valid password')
        return redirect('reset_password')
    return render(request, 'account/reset_password.html')


@login_required(login_url="/login/")
def dashboard(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, is_ordered=True)
        orders_s = Order.objects.filter(user=request.user, is_ordered=False)
        total_order = orders.count()
        on_the_way = orders_s.count()
        context = {
            "orders": orders,
            "total_order": total_order,
            "on_the_way": on_the_way
        }
        return render(request, 'dashboard/dashboard.html', context)
    return render(request, 'dashboard/dashboard.html')


@login_required(login_url="/login/")
def user_profile(request, username):
    user = None
    if request.user.is_authenticated:
        user = Account.objects.get(username=username)
    context = {
        "user": user
    }
    return render(request, 'dashboard/user_profile.html', context)


def change_password(request, username):
    if request.user.is_authenticated:
        if request.method == "POST":
            old_pass = request.POST['old_pass']
            new_pass = request.POST['new_pass']
            confirm_pass = request.POST['confirm_pass']
            user = Account.objects.get(username=username)
            if new_pass == confirm_pass:
                current_pass = user.check_password(old_pass)
                if current_pass:
                    user.set_password(new_pass)
                    user.save()
                    messages.success(request, 'new password set')
                    return redirect('user_profile', username=username)
                else:
                    messages.error(request, 'password not match')
                    return redirect('change_password', username=username)
            else:
                messages.error(request, 'Old password wrong')
                return redirect('change_password', username=username)
    return render(request, "dashboard/change_password.html")


@login_required(login_url="/login/")
def edit_profile(request, username):
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone_number = request.POST['phone_number']
            address_line = request.POST['address_liner']
            country = request.POST['country']
            state = request.POST['state']
            city = request.POST['city']

            user = Account.objects.get(username=username)
            user.phone_number=phone_number
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            user_profiles = UserProfile.objects.get(user=user)
            user_profiles.address_line_1 = address_line
            user_profiles.country = country
            user_profiles.state = state
            user_profiles.city = city
            user_profiles.save()
            messages.success(request, 'profile edit successfully')
            return redirect('user_profile', username=username)
    return render(request, "dashboard/edit_profile.html")


@login_required(login_url="/login/")
def profile_pic_change(request, username):
    if request.user.is_authenticated:
        if request.method == "POST":
            profile_pic = request.FILES['profile_pic']
            user = Account.objects.get(username=username)
            user_profiles = UserProfile.objects.get(user=user)
            user_profiles.profile_pic= profile_pic
            user_profiles.save()
    return redirect('edit_profile', username=username)


@login_required(login_url="/login/")
def cover_pic_change(request, username):
    if request.user.is_authenticated:
        if request.method == "POST":
            cover_pics = request.FILES['cover_pic']
            user = Account.objects.get(username=username)
            user_profiles = UserProfile.objects.get(user=user)
            user_profiles.cover_pic= cover_pics
            user_profiles.save()
    return redirect('edit_profile', username=username)


@login_required(login_url="/login/")
def order_details(request, user, order_number):
    if request.user.is_authenticated:
        order = Order.objects.get(order_number=order_number)
        order_products = OrderProduct.objects.filter(order=order)
        context = {
            "order": order,
            "order_products": order_products
        }
        return render(request, "dashboard/order_details.html", context)
    return render(request, "dashboard/order_details.html")


@login_required(login_url="/login/")
def order_profile(request, username):
    if request.user.is_authenticated:
        order_products = Order.objects.filter(user=request.user, is_ordered=True).order_by("-created_at")
        context = {
            "order_products": order_products
        }
        return render(request, "dashboard/order_profile.html", context)
    return render(request, "dashboard/order_profile.html")


@login_required(login_url="/login/")
def on_the_way(request, username):
    if request.user.is_authenticated:
        order_products = Order.objects.filter(user=request.user, is_ordered=False).order_by("-created_at")
        context = {
            "order_products": order_products
        }
        return render(request, "dashboard/order_profile.html", context)
    return render(request, "dashboard/order_profile.html")

