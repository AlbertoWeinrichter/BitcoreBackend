from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from slugify import slugify

from API.comments.models.comment import Comment
from API.notifications.models.notification import Notification
from API.notifications.serializers.notification import NotificationSerializer
from services.achievement_helper import achievement_check_ws


@receiver(post_save, sender=Comment)
def new_comment(sender, instance, **kwargs):
    # Check if it is the first comment I write
    sender_comment_total = len(Comment.objects.filter(user_id=instance.user.id))
    if sender_comment_total == 1 and instance.parent:
        user_to_send = instance.user

        # Objection!
        achievement_check_ws(user_to_send, "objection")

    # Check if its the answer to other comment
    if instance.parent:
        receiver_comment_total = len(Comment.objects.filter(user_id=instance.parent.user.id))
        user_to_send = instance.parent.user

        if receiver_comment_total == 1:
            achievement_check_ws(user_to_send, "its_on_like_donkey_kong")

        notification = Notification.objects.create(
            notification_type="comment",
            owner=user_to_send,
            new_post=instance,
            new_publication=instance.publication,
            notification_message="{publication_title}".format(publication_title=instance.publication.title)
        )

        channel_layer = get_channel_layer()
        serialized_notification = NotificationSerializer(notification).data
        async_to_sync(channel_layer.group_send)(
            slugify(user_to_send.username),
            {"type": "message",
             "data": serialized_notification},
        )
