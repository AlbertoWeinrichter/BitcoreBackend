from API.notifications.serializers.notification import NotificationSerializer
from API.notifications.models.notification import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
from slugify import slugify

logger = logging.getLogger(__name__)


# Method receives a user and an achievement.
# If the user did not already had that achievement, a notification will be created
# And a notification sent by channels
def achievement_check_ws(user, achievement_slug):
    from API.user.models.user import Achievement
    from API.user.models.user import AchievementMembership
    try:
        channel_layer = get_channel_layer()

        achievement, created = AchievementMembership.objects.get_or_create(
            user=user,
            achievement=Achievement.objects.get(slug=achievement_slug)
        )
        if created:
            notification = Notification.objects.create(
                notification_type="achievement",
                owner=user,
                new_achievement=achievement,
                notification_message=achievement.achievement.name
            )
            serialized_notification = NotificationSerializer(notification).data
            async_to_sync(channel_layer.group_send)(
                slugify(user.username),
                {"type": "message",
                 "data": serialized_notification},
            )
    except Exception as e:
        logger.error("Achievement check failed with error: {message}".format(message=e))
