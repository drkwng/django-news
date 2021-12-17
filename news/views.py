from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from .models import Article, Category, Comment, Newsletter
from .forms import CommentForm


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
    current_page = int(request.GET.get('page', 1))
    articles_on_page = 10

    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        last_articles = Article.objects.filter(
            categories__slug=cat_slug).order_by(
            '-pub_date').prefetch_related('categories')
        paginator = Paginator(last_articles, articles_on_page)
        page_obj = paginator.get_page(current_page)

    else:
        last_articles = Article.objects.all().order_by(
            '-pub_date').prefetch_related('categories')
        category = None
        paginator = Paginator(last_articles, articles_on_page)
        page_obj = paginator.get_page(current_page)

    context = {
        'category': category,
        'page_obj': page_obj,
        'paginator': paginator
    }

    return render(request, 'category.html', context)


def single_handler(request, post_slug):
    main_article = get_object_or_404(Article, slug=post_slug)

    try:
        prev_article = Article.objects.get(id=main_article.id-1)
    except ObjectDoesNotExist:
        prev_article = None

    try:
        next_article = Article.objects.get(id=main_article.id+1)
    except ObjectDoesNotExist:
        next_article = None

    context = {
        'article': main_article,
        'prev_article': prev_article,
        'next_article': next_article,
    }

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            data['article'] = main_article
            Comment.objects.create(**data)
            form = None

        else:
            messages.add_message(
                request, messages.INFO, 'Error in form fields')

    else:
        form = CommentForm()

    context['form'] = form

    return render(request, 'single.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'robots.txt', context,
                  content_type='text/plain')
