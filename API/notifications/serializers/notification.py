from rest_framework import serializers

from API.notifications.models.notification import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

    def to_representation(self, instance):
        data = super(NotificationSerializer, self).to_representation(instance)
        data.owner = instance

        if instance.notification_type == "achievement":
            data["new_achievement"] = instance.new_achievement.achievement.slug

        if instance.notification_type == "tag_content":
            data["new_publication"] = instance.new_publication.slug

        if instance.notification_type == "comment":
            data["new_publication"] = instance.new_publication.slug

        return data
