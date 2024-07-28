from .models import Category


def category(request):
    category_b = Category.objects.all()
    return dict(categories_base=category_b)
