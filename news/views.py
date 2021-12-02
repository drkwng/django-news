from django.shortcuts import render


def index_handler(request):
    context = {}
    return render(request, 'news/index.html', context)


def about_handler(request):
    context = {}
    return render(request, 'news/about.html', context)


def contact_handler(request):
    context = {}
    return render(request, 'news/contact.html', context)


def blog_handler(request):
    context = {}
    return render(request, 'news/blog.html', context)


def category_handler(request):
    context = {}
    return render(request, 'news/category.html', context)


def single_handler(request):
    context = {}
    return render(request, 'news/single.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'news/robots.txt', context,
                  content_type='text/plain')
