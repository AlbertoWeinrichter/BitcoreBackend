from API.notifications.models.notification import Notification
from API.notifications.serializers.notification import NotificationSerializer
from API.publication.models.publication import Publication
from API.publication.models.publication import PublicationImage
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from slugify import slugify
from PIL import Image
from io import BytesIO
import boto3


@receiver(post_save, sender=Publication)
def publish_publication(sender, instance, **kwargs):
    froala_snippet = """<p data-f-id="pbf" style="text-align: center; font-size: 14px; margin-top: 30px; opacity: 0.65; font-family: sans-serif;">Powered by <a href="https://www.froala.com/wysiwyg-editor?pb=1" title="Froala Editor">Froala Editor</a></p>"""

    instance.content.replace(froala_snippet, "")

    if len(PublicationImage.objects.filter(publication=instance)) == 0:
        PublicationImage.objects.create(
            publication=instance,
            path="",
            image_type="main"
        )
        PublicationImage.objects.create(
            publication=instance,
            path="",
            image_type="masonry"
        )
        PublicationImage.objects.create(
            publication=instance,
            path="",
            image_type="search"
        )
        PublicationImage.objects.create(
            publication=instance,
            path="",
            image_type="thumbnail"
        )
        PublicationImage.objects.create(
            publication=instance,
            path="",
            image_type="rrss"
        )

    from API.user.models.user import TagFollow
    tags = []
    tags += TagFollow.objects.filter(Q(tag__in=instance.publisher_tags.all()))
    tags += TagFollow.objects.filter(Q(tag__in=instance.developer_tags.all()))
    tags += TagFollow.objects.filter(Q(tag__in=instance.genre_tags.all()))
    tags += TagFollow.objects.filter(Q(tag__in=instance.title_tag.all()))
    tags += TagFollow.objects.filter(Q(tag__in=instance.review_platform_tags.all()))
    tags += TagFollow.objects.filter(Q(tag__in=instance.available_platform_tags.all()))
    tags += TagFollow.objects.filter(Q(tag__in=instance.tags.all()))

    users_to_call = list(set(user.follower for user in tags))
    channel_layer = get_channel_layer()

    for user in users_to_call:
        notification = Notification.objects.create(
            notification_type="tag_content",
            owner=user,
            new_publication=instance,
            notification_message="{publication_title}".format(publication_title=instance.title)
        )
        serialized_notification = NotificationSerializer(notification).data
        async_to_sync(channel_layer.group_send)(
            slugify(user.username),
            {"type": "message",
             "data": serialized_notification},
        )


@receiver(pre_save, sender=PublicationImage)
def optimise_images(sender, instance, **kwargs):
    if instance.path._file:
        # WEBP
        output = BytesIO()

        im = Image.open(instance.path.file)
        im.save(output, format='WEBP', lossless=True)
        output.seek(0)

        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name="eu-central-1"
        )
        s3 = session.resource('s3')
        bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

        path_webp = "media/" + instance.path.name.split(".")[0] + ".webp"
        bucket.put_object(Key=path_webp,
                          Body=output.getvalue(),
                          ACL='public-read')

        # JPEG2000
        output = BytesIO()

        im = Image.open(instance.path.file)
        im.convert("RGBA").save(output, 'JPEG2000', quality_mode='dB', quality_layers=[41])
        output.seek(0)

        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name="eu-central-1"
        )
        s3 = session.resource('s3')
        bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

        path_jpeg2k = "media/" + instance.path.name.split(".")[0] + ".jp2"
        bucket.put_object(Key=path_jpeg2k,
                          Body=output.getvalue(),
                          ACL='public-read')
