from django.db import models

from API.publication.models.publication import Publication


class PatreonImage(models.Model):
    url = models.CharField(max_length=999, default=None, null=True)
    thumbnail = models.CharField(max_length=999, default=None, null=True)
    minimum_level_needed = models.IntegerField(default=1)

    def __str__(self):
        return self.url


class Survey(models.Model):
    title = models.CharField(max_length=999, default=None, null=True)
    minimum_level_needed = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class PatreonOption(models.Model):
    name = models.CharField(max_length=999, default=None, null=True)
    minimum_level_needed = models.IntegerField(default=1)
    survey = models.ForeignKey(Survey,
                               related_name="survey_option",
                               on_delete=models.CASCADE
                               )


class PatreonUnlockedPublication(models.Model):
    minimum_level_needed = models.IntegerField(default=1)
    publication = models.ForeignKey(Publication,
                                    related_name="patreon_publication",
                                    on_delete=models.CASCADE
                                    )

    def __str__(self):
        return self.publication.title
