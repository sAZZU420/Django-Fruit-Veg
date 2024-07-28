from django.db import models
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count


class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    category_slug = models.SlugField(max_length=200, unique=True)
    category_image = models.ImageField(upload_to='category', blank=True)
    featured = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def category_count(self):
        categories = Product.objects.filter(category=self)
        count = categories.count()
        return count

    def get_url(self):
        return reverse('product_by_category', args=[self.category_slug])

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_slug = models.SlugField(max_length=200)
    description = models.TextField(max_length=500)
    price = models.FloatField()
    image = models.ImageField(upload_to='product')
    featured = models.BooleanField(default=False)
    best_product = models.BooleanField(default=False)
    in_stocks = models.IntegerField(blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(aver=Avg('rating'))
        avg = 0
        if reviews is not None:
            avg = float(reviews['aver'])
        return avg

    def average_count(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(counts=Count('rating'))
        count = 0
        if reviews is not None:
            count = int(reviews['counts'])
        return count

    def get_url(self):
        return reverse('product_details', args=[self.category.category_slug, self.product_slug])

    def __str__(self):
        return self.product_name


class Banner(models.Model):
    image = models.ImageField(upload_to='banner')
    banner_name = models.CharField(max_length=200, unique=True)
    banner_slug = models.SlugField(max_length=200, unique=True)
    discount = models.BooleanField(default=False)

    def __str__(self):
        return self.banner_name


class ReviewRating(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.product


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    product_image = models.ImageField(upload_to="product_gallery", blank=True)

    def __unicode__(self):
        return self.product

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
