from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from API.chat.models.chat import ChatMessage
from API.notifications.models.notification import Notification
from API.notifications.serializers.notification import NotificationSerializer
from slugify import slugify


@receiver(post_save, sender=ChatMessage)
def new_chat_message(sender, instance, **kwargs):
    from API.user.models.user import Achievement
    from API.user.models.user import AchievementMembership

    channel_layer = get_channel_layer()

    # Check if its an asnwer to other comment
    user_to_send = instance.user

    # ACHIEVEMENT: GOD MODE
    if instance.content == 'iddqd':
        god_mode, created = AchievementMembership.objects.get_or_create(
            user=user_to_send,
            achievement=Achievement.objects.get(slug="god_mode")
        )
        if created:
            notification = Notification.objects.create(
                notification_type="achievement",
                owner=user_to_send,
                new_achievement=god_mode,
                notification_message=god_mode.achievement.name
            )
            serialized_notification = NotificationSerializer(notification).data
            async_to_sync(channel_layer.group_send)(
                slugify(user_to_send.username),
                {"type": "message",
                 "data": serialized_notification},
            )
