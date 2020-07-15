from collections import defaultdict

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from API.notifications.models.notification import Notification
from API.notifications.serializers.notification import NotificationSerializer
from API.user.models.user import (Achievement, AchievementMembership, Border,
                                  BorderMembership, Preferences, TagFollow,
                                  Title, TitleMembership, User, UserFriendship)
from API.user.serializers.social import TagFollowSerializer


class PreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
        exclude = ("id", "user")


class BorderTrueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Border
        exclude = ("id", "title")


class BorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorderMembership
        fields = ('active', 'new')

    def to_representation(self, instance):
        data = super(BorderSerializer, self).to_representation(instance)
        data.update({"slug": instance.border.slug})

        return data


class AchievementTrueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        exclude = ("id", "title")


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementMembership
        fields = ('active', 'new')

    def to_representation(self, instance):
        data = super(AchievementSerializer, self).to_representation(instance)
        data.update({"slug": instance.achievement.slug})

        return data


class TitleTrueSerializer(serializers.ModelSerializer):
    border = BorderTrueSerializer(read_only=True, many=True)
    achievements = AchievementTrueSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('name', 'slug', 'border', 'achievements')

    def to_representation(self, instance):
        data = super(TitleTrueSerializer, self).to_representation(instance)

        return data


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleMembership
        fields = ('active', 'new')

    def to_representation(self, instance):
        data = super(TitleSerializer, self).to_representation(instance)
        data.update({
            'slug': instance.title.slug,
            'name': instance.title.name,
        })

        return data


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'avatar',
            'avatar_cropped'
        )

    def to_representation(self, instance):
        data = super(ProfileUserSerializer, self).to_representation(instance)
        if instance.id:
            title = TitleMembership.objects.filter(user=instance.id, active=True).first()
            border = BorderMembership.objects.filter(user=instance.id, active=True).first()
            achievements = AchievementMembership.objects.filter(user=instance.id, active=True)
            if title:
                data.update({"active_title": title.title.name})
            if border:
                data.update({"active_border": border.border.slug})

            achievements = [a.achievement.slug for a in achievements]

            while len(achievements) < 3:
                achievements.append("no_achievement")
            data.update({"active_achievements": achievements})

        return data


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFriendship
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    achievements = serializers.SerializerMethodField()
    titles = serializers.SerializerMethodField()
    borders = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()
    preferences = serializers.SerializerMethodField()
    notifications = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'titles',
            'achievements',
            'borders',
            'scores',
            'avatar',
            'avatar_cropped',
            'preferences',
            'patreon_level',
            'date_joined'
        )

    @staticmethod
    def get_achievements(user):
        ordered_by_category = defaultdict(list)
        achievements = AchievementMembership.objects.filter(user=user.id)
        for a in achievements:
            ordered_by_category[a.achievement.category].append(AchievementSerializer(a).data)
        return ordered_by_category

    @staticmethod
    def get_titles(user):
        title = TitleMembership.objects.filter(user=user.id)

        return TitleSerializer(title, many=True).data

    @staticmethod
    def get_borders(user):
        border = BorderMembership.objects.filter(user=user.id)

        return BorderSerializer(border, many=True).data

    @staticmethod
    def get_preferences(user):
        preferences = Preferences.objects.get(user=user.id)

        return PreferencesSerializer(preferences).data

    @staticmethod
    def get_scores(user):
        scores = user.get_scores(user.id)

        return scores

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        if instance.id:
            title = TitleMembership.objects.filter(user=instance.id, active=True).first()
            border = BorderMembership.objects.filter(user=instance.id, active=True).first()
            achievements = AchievementMembership.objects.filter(user=instance.id, active=True)
            if title:
                data.update({"active_title": title.title.name})
            if border:
                data.update({"active_border": border.border.slug})
            achievements = [a.achievement.slug for a in achievements]

            while len(achievements) < 3:
                achievements.append("no_achievement")
            data.update({"active_achievements": achievements})

            # New achievements shown as new only once
            achievements = AchievementMembership.objects.filter(user=instance.id, new=True)
            for a in achievements:
                a.new = False
                a.save()
            borders = AchievementMembership.objects.filter(user=instance.id, new=True)
            for b in borders:
                b.new = False
                b.save()
            titles = AchievementMembership.objects.filter(user=instance.id, new=True)
            for t in titles:
                t.new = False
                t.save()

            # already following or blocking?
            if not self.context == {}:
                try:
                    UserFriendship.objects.filter(follower=instance, follow=True)
                    data.update({"already_following": True})
                except UserFriendship.DoesNotExist:
                    data.update({"already_following": False})

                try:
                    UserFriendship.objects.filter(follower=instance, follow=True)
                    data.update({"already_blocking": True})
                except UserFriendship.DoesNotExist:
                    data.update({"already_blocking": False})

        return data


class UserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',
                  'username',
                  )


class UserSerializerLogin(UserSerializer):
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(user):
        """
        Get token
        """

        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ('token', 'username', 'avatar_cropped', 'email')


class UserSerializerRefreshToken(UserSerializer):
    token = serializers.SerializerMethodField()

    @staticmethod
    def refresh_token(user):
        """
        Refresh token
        """

        token, created = Token.objects.update(user=user, token="hey")
        return token.key

    class Meta:
        model = User
        fields = (
            'token',
            'username',
            'avatar',
            'avatar_cropped',
        )

    def to_representation(self, instance):
        data = super(UserSerializerRefreshToken, self).to_representation(instance)
        if instance.id:
            title = TitleMembership.objects.filter(user=instance.id, active=True).first()
            border = BorderMembership.objects.filter(user=instance.id, active=True).first()
            achievements = AchievementMembership.objects.filter(user=instance.id, active=True)
            if title:
                data.update({"active_title": title.title.name})
            if border:
                data.update({"active_border": border.border.slug})
            data.update({"active_achievements": [a.achievement.slug for a in achievements]})

        return data


class UserSerializerFollowUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def save(self):
        user = self.context["request"].user
        self.validated_data.update({"user": user})

        follow_user = User.objects.get(username=self.data["follow_user"])
        self.validated_data.update({"followed_users": follow_user})

        self.create(self.validated_data)


class UserFriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFriendship
        exclude = ("id", "friend")

    def to_representation(self, instance):
        data = super(UserFriendshipSerializer, self).to_representation(instance)

        data.update({"friend": ProfileUserSerializer(instance.friend).data})
        data.update({"follower": ProfileUserSerializer(User.objects.get(id=instance.follower.id)).data})

        return data


class CompleteUserSerializer(serializers.ModelSerializer):
    achievements = serializers.SerializerMethodField()
    titles = serializers.SerializerMethodField()
    borders = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()
    preferences = serializers.SerializerMethodField()
    subscriptions = serializers.SerializerMethodField()
    achievement_list = serializers.SerializerMethodField()
    notifications = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'titles',
            'achievements',
            'borders',
            'scores',
            'avatar',
            'avatar_cropped',
            'preferences',
            'subscriptions',
            'patreon_level',
            'date_joined',
            'achievement_list',
            'notifications',
            'new_user',
            'auth_id'
        )

    @staticmethod
    def get_notifications(user):
        notifications = Notification.objects.filter(owner_id=user.id)[:5]
        if len(notifications) > 0:
            return NotificationSerializer(notifications, many=True).data
        else:
            return {}

    @staticmethod
    def get_achievement_list(user):
        achievements = Achievement.objects.all()
        titles = Title.objects.all()

        achievement_list = {
            "achievements": AchievementTrueSerializer(achievements, many=True).data,
            "titles": TitleTrueSerializer(titles, many=True).data
        }

        return achievement_list

    @staticmethod
    def get_subscriptions(user):
        friendships = UserFriendship.objects.filter(follower=user, follow=True)
        serialized_friends = UserFriendshipSerializer(friendships, many=True).data

        blocked = UserFriendship.objects.filter(follower=user, block=True)
        serialized_blocked = UserFriendshipSerializer(blocked, many=True).data

        followers = UserFriendship.objects.filter(friend=user, follow=True)
        serialized_followers = UserFriendshipSerializer(followers, many=True).data

        followed_tags = TagFollow.objects.filter(follower=user)
        serialized_tags = TagFollowSerializer(followed_tags, many=True).data
        subscriptions = {
            "friendships": serialized_friends,
            "followers": serialized_followers,
            "blocked": serialized_blocked,
            "followed_tags": serialized_tags
        }

        return subscriptions

    @staticmethod
    def get_achievements(user):
        achievements = AchievementMembership.objects.filter(user=user.id)

        serialized_achievements = AchievementSerializer(achievements, many=True).data

        return serialized_achievements
        # ordered_by_category = defaultdict(list)
        # for a in achievements:
        #     ordered_by_category[a.achievement.category].append(AchievementSerializer(a).data)
        # return ordered_by_category

    @staticmethod
    def get_titles(user):
        title = TitleMembership.objects.filter(user=user.id)

        return TitleSerializer(title, many=True).data

    @staticmethod
    def get_borders(user):
        border = BorderMembership.objects.filter(user=user.id)

        return BorderSerializer(border, many=True).data

    @staticmethod
    def get_preferences(user):
        preferences = Preferences.objects.get(user=user.id)

        return PreferencesSerializer(preferences).data

    @staticmethod
    def get_scores(user):
        scores = user.get_scores(user.id)

        return scores

    def to_representation(self, instance):
        data = super(CompleteUserSerializer, self).to_representation(instance)
        if instance.id:
            title = TitleMembership.objects.filter(user=instance.id, active=True).first()
            border = BorderMembership.objects.filter(user=instance.id, active=True).first()
            achievements = AchievementMembership.objects.filter(user=instance.id, active=True)
            if title:
                data.update({"active_title": title.title.name})
            if border:
                data.update({"active_border": border.border.slug})
            achievements = [a.achievement.slug for a in achievements]

            while len(achievements) < 3:
                achievements.append("no_achievement")
            data.update({"active_achievements": achievements})

            # New achievements shown as new only once
            achievements = AchievementMembership.objects.filter(user=instance.id, new=True)
            for a in achievements:
                a.new = False
                a.save()
            borders = AchievementMembership.objects.filter(user=instance.id, new=True)
            for b in borders:
                b.new = False
                b.save()
            titles = AchievementMembership.objects.filter(user=instance.id, new=True)
            for t in titles:
                t.new = False
                t.save()

            # already following or blocking?
            if not self.context == {}:
                try:
                    UserFriendship.objects.filter(follower=instance, follow=True)
                    data.update({"already_following": True})
                except UserFriendship.DoesNotExist:
                    data.update({"already_following": False})

                try:
                    UserFriendship.objects.filter(follower=instance, follow=True)
                    data.update({"already_blocking": True})
                except UserFriendship.DoesNotExist:
                    data.update({"already_blocking": False})

        return data
