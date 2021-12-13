from django.shortcuts import render
from .models import Article, Category

from django.db.models import Count


def index_handler(request):
    last_articles = Article.objects.all().order_by(
        '-pub_date')[:8].prefetch_related('categories')

    cat_list = Category.objects.annotate(count=Count(
        'article__id')).order_by('count')

    context = {
        'last_articles': last_articles,
        'menu_categories': cat_list
    }
    return render(request, 'index.html', context)


def about_handler(request):
    context = {}
    return render(request, 'about.html', context)


def contact_handler(request):
    context = {}
    return render(request, 'contact.html', context)


def blog_handler(request):
    last_articles = Article.objects.all().order_by(
        '-pub_date')[:10].prefetch_related('categories')

    context = {'last_articles': last_articles}

    return render(request, 'blog.html', context)


def category_handler(request, cat_slug):
    context = {}
    return render(request, 'category.html', context)


def single_handler(request, slug):
    context = {}
    return render(request, 'single.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'robots.txt', context,
                  content_type='text/plain')
