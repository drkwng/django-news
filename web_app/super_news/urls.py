"""news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import index, sitemap

from news import views
from news.sitemaps import sitemaps
from news.context_processor import subscribe

from django.views.decorators.cache import cache_page

import debug_toolbar


urlpatterns = [
    path('', cache_page(60*60)(views.IndexView.as_view()), name='homepage'),
    path('about/', cache_page(60*60)(views.AboutView.as_view()), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),

    path('blog/', views.BlogListView.as_view(), name='blog'),

    path('post/<post_slug>/', views.PageDetailView.as_view(), name='article'),
    path('tag/<slug>/', views.TagListView.as_view(), name='tag'),
    path('search/', views.SearchView.as_view(), name='search'),

    path('robots.txt', views.RobotsView.as_view()),

    path('sitemap.xml', cache_page(86400)(index), {'sitemaps': sitemaps,
                                                   'sitemap_url_name': 'sitemaps'}),
    path('sitemap-<section>.xml', cache_page(86400)(sitemap), {'sitemaps': sitemaps},
         name='sitemaps'),

    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),

    path('accounts/', include('authors.urls')),

    path('subscribe/', subscribe, name='subscribe'),

    path('<cat_slug>/', views.CategoryListView.as_view(), name='category'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
