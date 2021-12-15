from django.db import models
from string import punctuation


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    in_menu = models.BooleanField(default=True)
    order = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Author(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars')
    bio = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    content_words_count = models.IntegerField(null=True, blank=True)
    short_description = models.TextField()
    main_image = models.ImageField(upload_to='images')
    pub_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.comment[:20]


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribe_date = models.DateTimeField(auto_now_add=True)
    unsubscribe_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.name



