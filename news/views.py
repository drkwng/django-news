from django.shortcuts import render


def index_handler(request):
    context = {}
    return render(request, 'index.html', context)


def about_handler(request):
    context = {}
    return render(request, 'about.html', context)


def contact_handler(request):
    context = {}
    return render(request, 'contact.html', context)


def blog_handler(request):
    context = {}
    return render(request, 'blog.html', context)


def category_handler(request):
    context = {}
    return render(request, 'category.html', context)


def single_handler(request):
    context = {}
    return render(request, 'single.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'robots.txt', context,
                  content_type='text/plain')
