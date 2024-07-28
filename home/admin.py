from django.contrib import admin
from .models import Product, Category, ReviewRating, Banner, ProductGallery
import admin_thumbnails


@admin_thumbnails.thumbnail('product_image')
class ProductGalleryView(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "category", "price", "featured", "best_product", "in_stocks", "in_stock", "create_date")
    list_filter = ("product_name", "price", "featured", "best_product", "in_stock",)
    list_editable = ("featured", "best_product", "in_stocks", "in_stock",)
    list_per_page = 20
    ordering = ["-create_date"]
    inlines = [ProductGalleryView]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "featured", "create_date")
    list_filter = ("category_name", "featured")
    list_per_page = 20
    ordering = ["-create_date"]


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rating", "status", "create_at")
    list_filter = ("user", "product", "rating", "status",)
    list_per_page = 20
    ordering = ["-create_at"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(Banner)
admin.site.register(ProductGallery)
