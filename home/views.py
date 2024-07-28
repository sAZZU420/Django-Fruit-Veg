from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Banner, ReviewRating, ProductGallery
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def home(request):
    category = Category.objects.all().order_by('category_name')
    product = Product.objects.all()
    banner = Banner.objects.all()

    context = {
        "categories": category,
        "products": product,
        "banners": banner
    }
    return render(request, 'home.html', context)


def store(request, category_slug=None):
    featured_products = Product.objects.all()
    if category_slug:
        category = Category.objects.all().order_by('category_name')
        product = Product.objects.filter(category__category_slug=category_slug)
        paginator = Paginator(product, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        total_page = page_obj.paginator.num_pages
    else:
        category = Category.objects.all().order_by('category_name')
        product = Product.objects.all()
        paginator = Paginator(product, 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        total_page = page_obj.paginator.num_pages

    context = {
        "categories": category,
        "featured_products": featured_products,
        "products": page_obj,
        "total_page": [n+1 for n in range(total_page)]
    }
    return render(request, 'store.html', context)


def product_details(request, category_slug, product_slug):
    single_product = Product.objects.get(category__category_slug=category_slug, product_slug=product_slug)
    product = Product.objects.all()
    product_gallery = ProductGallery.objects.filter(product=single_product)
    category = Category.objects.all().order_by('category_name')
    product_rating = ReviewRating.objects.filter(product=single_product, status=True)
    context = {
        "single_product": single_product,
        "products": product,
        "categories": category,
        "product_ratings": product_rating,
        "product_gallery": product_gallery,
    }
    return render(request, 'product_details.html', context)


def search_product(request):
    featured_products = Product.objects.all()
    category = Category.objects.all().order_by('category_name')
    products = None
    keywords = None
    if request.method == "GET":
        keywords = request.GET['keywords']
        if keywords:
            products = Product.objects.filter(Q(description__icontains=keywords) | Q(product_name__icontains=keywords) | Q(category__category_slug__icontains=keywords))
            print(products)
    context = {
        "categories": category,
        "featured_products": featured_products,
        'products': products,
        'keywords': keywords
    }
    print(context['products'])
    return render(request, 'store.html', context)


@login_required(login_url="/login/")
def review_rating(request, product_slug):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        review = request.POST['review']
        rating = request.POST['rate']
        product = Product.objects.get(product_slug=product_slug)
        if request.user.is_authenticated:
            try:
                review_rate = ReviewRating.objects.get(user=request.user, product=product)
                review_rate.rating = rating
                review_rate.review = review
                review_rate.save()
            except ReviewRating.DoesNotExist:
                review_rate = ReviewRating.objects.create(
                    user=request.user,
                    product=product,
                    review=review,
                    rating=rating,
                    ip=request.META['REMOTE_ADDR'],
                    status=True,
                )
                review_rate.save()
    return redirect(url)
