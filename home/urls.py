from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='product_by_category'),
    path('product_details/<slug:category_slug>/<slug:product_slug>', views.product_details, name='product_details'),
    path('search/', views.search_product, name='search'),
    path('rating/<product_slug>/', views.review_rating, name='rating'),
]
