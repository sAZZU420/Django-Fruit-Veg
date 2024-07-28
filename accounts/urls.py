from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('activate/<uuid64>/<token>/', views.activate, name='activate'),

    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),

    path('dashboard/', views.dashboard, name="dashboard"),

    path('user_profile/<username>', views.user_profile, name="user_profile"),
    path('user_profile/<username>/change_password/', views.change_password, name="change_password"),
    path('user_profile/<username>/edit_profile/', views.edit_profile, name="edit_profile"),
    path('user_profile/<username>/profile_pic_change/', views.profile_pic_change, name="profile_pic_change"),
    path('user_profile/<username>/cover_pic_change/', views.cover_pic_change, name="cover_pic_change"),

    path('orders/<username>/order_profile/', views.order_profile, name="order_profile"),
    path('orders/<username>/on_the_way/', views.on_the_way, name="on_the_way"),
    path('orders/<user>/order_profile/order_details//<order_number>', views.order_details, name="order_details"),

    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('email_verification/<uuid64>/<token>/', views.email_verification, name="email_verification"),
    path('reset_password/', views.reset_password, name="reset_password"),
]
