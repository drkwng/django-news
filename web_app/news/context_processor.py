from .models import Category, Article
from django.db.models import Count


def menu_categories(request):
    cat_list = Category.objects.annotate(count=Count(
        'article__id')).order_by('-count')

    return {'menu_categories': cat_list}


def recent_posts(request):
    last_articles = Article.objects.all().order_by(
        '-pub_date')[:4].prefetch_related('categories')

    return {
        'recent_posts': last_articles
    }
