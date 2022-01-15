from .models import Category, Article, Newsletter, Tag
from .forms import NewsletterForm

from django.db.models import Count

from django.shortcuts import render
from django.http import HttpResponseRedirect


def menu_categories(request):
    cat_list = Category.objects.annotate(count=Count(
        'article__id')).order_by('-count')

    return {'menu_categories': cat_list}


def tags_linking(request):
    tags_list = Tag.objects.order_by('?')[:10]

    return {'tags_list': tags_list}


def recent_posts(request):
    last_articles = Article.objects.all().order_by(
        '-pub_date')[:4].prefetch_related('categories')

    return {
        'recent_posts': last_articles
    }


def subscribe(request):
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            data = newsletter_form.cleaned_data
            Newsletter.objects.create(**data)
            # Newsletter.objects.create(newsletter_form.cleaned_data['email'])
            return HttpResponseRedirect('/')

        else:
            context = {'form': newsletter_form}
            return render(request, 'homepage', context)

    else:
        return render(request, 'homepage')
