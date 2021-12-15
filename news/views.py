from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Article, Category, Comment

from django.db.models import Count


def index_handler(request):
    last_articles = Article.objects.all().order_by(
        '-pub_date')[:8].prefetch_related('categories')

    context = {
        'last_articles': last_articles
    }
    return render(request, 'index.html', context)


def about_handler(request):
    context = {}
    return render(request, 'about.html', context)


def contact_handler(request):
    context = {}
    return render(request, 'contact.html', context)


def blog_handler(request, **kwargs):
    cat_slug = kwargs.get('cat_slug')
    category = ''
    if cat_slug:
        category = Category.objects.get(slug=cat_slug)
        last_articles = Article.objects.filter(
            categories__slug=cat_slug).order_by(
            '-pub_date')[:10].prefetch_related('categories')
    else:
        last_articles = Article.objects.all().order_by(
            '-pub_date')[:10].prefetch_related('categories')

    context = {
        'last_articles': last_articles,
        'category': category
    }

    return render(request, 'category.html', context)


def single_handler(request, post_slug):
    main_article = Article.objects.get(slug=post_slug)

    try:
        prev_article = Article.objects.get(id=main_article.id-1)
    except ObjectDoesNotExist:
        prev_article = None

    try:
        next_article = Article.objects.get(id=main_article.id+1)
    except ObjectDoesNotExist:
        next_article = None

    # comments = Comment.objects.get(article_id=main_article.id)

    context = {
        'article': main_article,
        'prev_article': prev_article,
        'next_article': next_article,
        # 'comments': comments
    }
    return render(request, 'single.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'robots.txt', context,
                  content_type='text/plain')
