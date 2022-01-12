from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Article


html_strip = analyzer(
    'html_strip',
    tokenizer='standard',
    filter=['lowercase', 'stop', 'snowball'],
    char_filter=['html_strip']
)


@registry.register_document
class ArticleDocument(Document):

    content = fields.TextField(analyzer=html_strip)

    class Index:
        # Name of the Elasticsearch index
        name = 'articles'

    class Django:
        model = Article

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
            # 'content',
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
