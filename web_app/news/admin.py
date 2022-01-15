from django.contrib import admin
from django.utils.html import format_html
from threading import Thread

from news.crawlers import coindesk_crawler

from django_summernote.admin import SummernoteModelAdmin

from .models import Article, Category, Newsletter, Comment, Tag


def count_words(modeladmin, request, queryset):
    for object in queryset:
        text = object.content.replace('<p>', '').replace('</p>', '')
        words = text.split()
        object.content_words_count = len(words)
        object.save()


count_words.short_description = 'Count words in article'


def get_fresh_news(modeladmin, request, queryset):
    for object in queryset:
        if object.name == 'Coindesk':
            Thread(target=coindesk_crawler.run(), args=()).start()


get_fresh_news.short_description = 'Get fresh articles'


def moderate_comments(modeladmin, request, queryset):
    for object in queryset:
        object.is_moderated = True
        object.save()


moderate_comments.short_description = 'Moderate comments'


class CommentArticleInline(admin.TabularInline):
    model = Comment


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', 'short_description')
    list_display = ('name', 'image_code', 'pub_date',
                    'author', 'content_words_count', 'count_unique_words')

    list_filter = ('author', 'pub_date', 'categories')
    search_fields = ('name', )
    actions = (count_words, )
    inlines = (CommentArticleInline, )

    def image_code(self, object):
        return format_html(
            '<img src="{}" style="max-width:80px" />',
            object.main_image.url
        )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'in_menu', 'order', 'articles_count')
    list_filter = ('in_menu', 'order')
    search_fields = ('name',)
    list_editable = ('order', )
    readonly_fields = ('order', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('article_set')

    def articles_count(self, object):
        return object.article_set.all().count()


class CommentAdmin(admin.ModelAdmin):
    list_display = ('is_moderated', 'pub_date',
                    'comment', 'name', 'article')
    actions = (moderate_comments, )


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Newsletter)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
