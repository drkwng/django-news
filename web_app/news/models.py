from django.db import models
from string import punctuation
from authors.models import Author

from django.urls import reverse


class SEONews(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    canonical_url = models.URLField(blank=True, null=True)
    meta_robots = models.CharField(max_length=50, blank=True, null=True)
    h1 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class Category(SEONews):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    in_menu = models.BooleanField(default=True)
    order = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category', args=(self.slug, ))


class Article(SEONews):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    content_words_count = models.IntegerField(null=True, blank=True)
    short_description = models.TextField()
    main_image = models.ImageField(upload_to='images')
    pub_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Author, blank=True, null=True, on_delete=models.CASCADE, related_name='articles')

    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article', args=(self.slug, ))

    def count_unique_words(self):
        text = self.content.replace('<p>', '').replace('</p>', '')
        for symbol in punctuation:
            text = text.replace(symbol, '')
        words = text.split()
        return len(set(words))


class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.CharField(max_length=255)
    comment = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
    is_moderated = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.comment[:20]


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribe_date = models.DateTimeField(auto_now_add=True)
    unsubscribe_date = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.email


class Tag(SEONews):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', args=(self.slug, ))



