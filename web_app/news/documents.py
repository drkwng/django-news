from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Article


@registry.register_document
class ArticleDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'articles'
        # See Elasticsearch Indices API reference for available settings

    class Django:
        model = Article

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
            'content',
            'pub_date',
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000
