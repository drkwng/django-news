from django.contrib.sitemaps import Sitemap
from news.models import Article, Category, Tag


class ArticlesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    limit = 25000

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.pub_date


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Category.objects.all()


class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Tag.objects.all()


sitemaps = {'articles': ArticlesSitemap,
            'categories': CategorySitemap,
            'tags': TagSitemap}
