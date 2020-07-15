import tagulous.models
from django.db import models


class CustomTag(tagulous.models.TagModel):
    class TagMeta:
        force_lowercase = True


class ContactForm(models.Model):
    """
    Contact form
    """
    submission_types = {
        ("tecnico", "tecnico"),
        ("particular", "particular"),
        ("empresa", "empresa"),
        ("inapropiado", "inapropiado"),
        ("patreon_link", "patreon_link"),
        ("otros", "otros")
    }

    content = models.TextField()
    subject = models.TextField()
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    submission_type = models.CharField(max_length=100, choices=submission_types)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)


class Quote(models.Model):
    content = models.CharField(max_length=100)
    author = models.CharField(max_length=100)


class Ad(models.Model):
    ad_types = {
        ("widget", "widget"),
        ("banner", "banner")
    }
    ad_type = models.CharField(max_length=100, choices=ad_types)
    image_path = models.CharField(max_length=9999)
