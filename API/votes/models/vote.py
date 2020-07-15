from django.conf import settings
from django.db import models

from API.utils import constants


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(choices=constants.VOTE_VALUE_CHOICES)

    class Meta:
        abstract = True
