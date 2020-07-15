from __future__ import unicode_literals

import tagulous.models
from django.urls import reverse
from froala_editor.fields import FroalaField
from django.db import models


class Publication(models.Model):
    def get_absolute_url(self):
        return reverse('publication_detail', args=(self.slug,))

    # TODO: change for correct article types
    types = [
        ('noticia', 'noticia'),
        ('articulo', 'artículo'),
        ('análisis', 'análisis'),
    ]

    publication_type = models.CharField(max_length=100, choices=types)
    slug = models.SlugField()
    author = models.ForeignKey('user.user',
                               related_name="author",
                               on_delete=models.CASCADE)

    title = models.CharField(max_length=100, default=None, null=True, blank=True)
    subtitle = models.CharField(max_length=100, default=None, null=True, blank=True)
    game_release_name = models.CharField(max_length=100, default=None, null=None, blank=True)
    game_release_date = models.DateTimeField(null=None, blank=True)
    publication_date = models.DateTimeField(null=None, blank=True)

    title_tag = tagulous.models.TagField(to="general.customtag", related_name="title_tag", default=None, blank=True)
    genre_tags = tagulous.models.TagField(to="general.customtag", related_name="genre_tags", default=None, blank=True)
    developer_tags = tagulous.models.TagField(to="general.customtag", related_name="developer_tags", default=None,
                                              blank=True)
    publisher_tags = tagulous.models.TagField(to="general.customtag", related_name="publisher_tags", default=None,
                                              blank=True)
    review_platform_tags = tagulous.models.TagField(to="general.customtag", related_name="review_platform_tags",
                                                    default=None,
                                                    blank=True)
    available_platform_tags = tagulous.models.TagField(to="general.customtag", related_name="available_platform_tags",
                                                       default=None, blank=True)

    tags = tagulous.models.TagField(to="general.customtag", related_name="tags", default=None, blank=True)

    content = FroalaField()

    masonry_snippet = models.CharField(max_length=140, default=None, null=True)
    masonry_size = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class ProsAndCons(models.Model):
    types = [
        ('pro', 'pro'),
        ('con', 'contra')
    ]

    publication = models.ForeignKey(Publication,
                                    related_name="pros_and_cons",
                                    on_delete=models.CASCADE,
                                    )
    type = models.CharField(max_length=100, default=None, null=True, choices=types)
    content = models.CharField(max_length=9999, default=None, null=True)

    def __str__(self):
        return self.publication.slug + " - " + self.type


class PublicationScore(models.Model):
    publication = models.ForeignKey(Publication,
                                    related_name="scores",
                                    on_delete=models.CASCADE
                                    )
    types = [
        ('adiccion', 'ADICCIÓN'),
        ('ambientacion', 'AMBIENTACIÓN'),
        ('combate', 'COMBATE'),
        ('dificultad', 'DIFICULTAD'),
        ('equipo', 'EQUIPO'),
        ('estrategia', 'ESTRATEGIA'),
        ('terror', 'TERROR'),
        ('puzzles', 'PUZZLES'),
        ('monstruos', 'MONSTRUOS'),
        ('narrativa', 'NARRATIVA'),
    ]

    name = models.CharField(max_length=100, choices=types)
    types = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    value = models.IntegerField(choices=types)
    description = models.CharField(max_length=999, default=None, null=True)

    def __str__(self):
        return self.publication.slug + " - " + self.name


class PublicationImage(models.Model):
    publication = models.ForeignKey(Publication,
                                    related_name="images",
                                    on_delete=models.CASCADE
                                    )
    path = models.ImageField(default=None, null=True, max_length=9999)

    types = [
        ('main', 'main'),
        ('masonry', 'masonry'),
        ('search', 'search'),
        ('thumbnail', 'thumbnail'),
        ('rrss', 'rrss'),
    ]

    image_type = models.CharField(max_length=100, choices=types)

    def __str__(self):
        return self.publication.slug + " - " + self.image_type


# ALWAYS SKIP ISORT AND ALWAYS IMPORT AT THE END OF MODELS OR SIGNALS GIVE A CIRCULAR DEPENDENCY ERROR
from API.publication.signals.publication import publish_publication # noqa isort:skip
from API.publication.signals.publication import optimise_images # noqa isort:skip
