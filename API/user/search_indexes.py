from django.contrib.auth import get_user_model
from django.utils import timezone

from haystack import indexes

User = get_user_model()


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    date_joined = indexes.DateTimeField(model_attr='date_joined')
    username = indexes.CharField(model_attr='username')

    username_auto = indexes.EdgeNgramField(model_attr='username')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(date_joined__lte=timezone.now())