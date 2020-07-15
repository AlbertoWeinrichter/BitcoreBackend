from django.utils import timezone
from haystack import indexes

from API.publication.models.publication import Publication


class PublicationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    slug = indexes.CharField(model_attr='slug')
    title = indexes.CharField(model_attr='title')

    title_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Publication

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(publication_date__lte=timezone.now())
