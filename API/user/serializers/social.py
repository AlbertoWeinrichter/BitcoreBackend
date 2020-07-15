from rest_framework import serializers

from API.general.models.general import CustomTag
from API.user.models.user import TagFollow, User, UserFriendship


class UserFriendshipSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = UserFriendship
        exclude = ('follower', 'friend')

    def create(self, validated_data):
        follower_user = self.context["request"].user
        friend = User.objects.get(username=self.context["request"].data["friend"])

        user_friendship, created = UserFriendship.objects.get_or_create(
            follower=follower_user,
            friend=friend,
        )
        user_friendship.follow = self.initial_data["follow"]
        user_friendship.block = self.initial_data["block"]
        user_friendship.save()

        return user_friendship


class TagFollowSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = TagFollow
        exclude = ('follower', 'tag')

    def create(self, validated_data):
        follower_user = self.context["request"].user
        followed_tag = CustomTag.objects.get(slug=self.initial_data["tag"])

        tag_follow, created = TagFollow.objects.get_or_create(
            follower=follower_user,
            tag=followed_tag)
        if not created:
            tag_follow.delete()

        return tag_follow


class TagFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagFollow
        exclude = ("id", "follower")

    def to_representation(self, instance):
        data = super(TagFollowSerializer, self).to_representation(instance)
        data.update({
            "tag_name": instance.tag.name,
            "tag": instance.tag.slug
        })

        return data
