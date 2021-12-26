from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse

from django.contrib import messages

from .models import Article, Category, Comment
from .forms import CommentForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_articles'] = Article.objects.all().order_by(
            '-pub_date')[:8].prefetch_related('categories')
        return context


class BlogListView(ListView):
    template_name = 'category.html'
    model = Article
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().\
            prefetch_related('categories')


class CategoryListView(ListView, SingleObjectMixin):
    template_name = 'category.html'
    model = Article
    ordering = '-pub_date'
    paginate_by = 10
    slug_url_kwarg = 'cat_slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = self.object.article_set.all().\
            prefetch_related('categories')
        return super().get_queryset()


class PageDetailView(FormMixin, DetailView):
    template_name = 'single.html'
    model = Article
    slug_url_kwarg = 'post_slug'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            prev_article = Article.objects.get(id=self.object.id - 1)
        except ObjectDoesNotExist:
            prev_article = None
        try:
            next_article = Article.objects.get(id=self.object.id + 1)
        except ObjectDoesNotExist:
            next_article = None
        context['prev_article'] = prev_article
        context['next_article'] = next_article
        context['comments'] = self.object.comments.filter(is_moderated=True)
        return context

    def post(self, request, *arts, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.success(self.request, 'The changes have been saved.')
        return reverse('article', kwargs={'post_slug': context['object'].slug})

    def form_valid(self, form):
        data = form.cleaned_data
        data['article'] = self.object
        Comment.objects.create(**data)
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class RobotsView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'

