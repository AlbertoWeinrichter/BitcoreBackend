from API.general.models.general import CustomTag
from haystack import indexes


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr="name")
    slug = indexes.CharField(model_attr="slug")

    text_auto = indexes.EdgeNgramField(model_attr='slug')

    def get_model(self):
        return CustomTag

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
