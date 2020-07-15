import tagulous.models
from django.db import models

from API.publication.models.publication import Publication


class Release(models.Model):
    types = [
        ('release', 'release'),
        ('event', 'event'),
    ]

    release_date = models.DateField()
    release_type = models.CharField(max_length=999, choices=types)
    title = models.CharField(max_length=999)
    important_tags = tagulous.models.TagField(to="general.customtag",
                                              related_name="release_important_tags", default=None,
                                              blank=True)
    other_tags = tagulous.models.TagField(to="general.customtag",
                                          related_name="release_other_tags", default=None, blank=True)
    snippet = models.CharField(max_length=999, blank=True, null=True)
    description = models.TextField(blank=True, null=True, )
    video = models.CharField(max_length=999, blank=True, null=True)
    external_link = models.CharField(max_length=999, blank=True, null=True)
    review_link = models.ForeignKey(Publication,
                                    blank=True, null=True,
                                    related_name="review_link",
                                    on_delete=models.CASCADE
                                    )

    def __str__(self):
        return self.title


class ReleaseImage(models.Model):
    release = models.ForeignKey(Release,
                                related_name="release_images",
                                on_delete=models.CASCADE
                                )
    path = models.ImageField(default=None, null=True)
    types = [
        ('gallery', 'Gallery'),
        ('main', 'Main'),
        ('thumbnail', 'Thumbnail'),
    ]

    image_type = models.CharField(max_length=100, choices=types, default="gallery")

    def __str__(self):
        return self.release.title + " - " + self.image_type
