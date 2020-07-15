import logging

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.contrib.postgres.fields import ArrayField
from django.db import models

from API.general.models.general import CustomTag
from API.votes.models.post_vote import PostVote

logger = logging.getLogger(__name__)


# TODO: THIS WILL REQUIRE MIGRATIONS TO BE PERFORMED
# TODO: THERE MUST BE A BETTER WAY TO IMPLEMENT SCORE ARTICLE AND CHRISTMAS ACHIEVEMENTS
class User(AbstractBaseUser, PermissionsMixin):
    auth_id = models.CharField(max_length=255, editable=False, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    avatar_cropped = models.CharField(max_length=255, blank=True, null=True)
    patreon_level = models.IntegerField(default=0)

    new_user = models.BooleanField(default=True)

    christmas_achievement_1 = models.BooleanField(default=False, blank=True)
    christmas_achievement_2 = models.BooleanField(default=False, blank=True)
    score_articles_seen = ArrayField(models.CharField(default="{}", max_length=100),
                                     default=list,
                                     blank=True,
                                     null=True)
    score_article_achievement_owner = models.BooleanField(default=False)

    USERNAME_FIELD = 'auth_id'

    objects = UserManager()


    @staticmethod
    def get_scores(user_id):
        user = User.objects.get(id=user_id)
        followed_users = len(UserFriendship.objects.filter(follower=user, follow=True))
        follower_users = len(UserFriendship.objects.filter(friend=user, follow=True))
        followed_tag = len(TagFollow.objects.filter(follower=user))
        post_likes = len(PostVote.objects.filter(user=user, value=1))
        total_titles = len(TitleMembership.objects.filter(user=user.id))
        total_achievements = len(AchievementMembership.objects.filter(user=user.id))
        total_borders = len(BorderMembership.objects.filter(user=user.id))

        scores = {
            "followed_users": followed_users,
            "follower_users": follower_users,
            "followed_tags": followed_tag,
            "post_likes": post_likes,
            "total_titles": total_titles,
            "total_achievements": total_achievements,
            "total_borders": total_borders,
        }

        return scores

    class Meta:
        app_label = 'user'

    def __str__(self):
        return self.username


class Title(models.Model):
    name = models.CharField(max_length=999, blank=True)
    slug = models.CharField(max_length=999, blank=True)
    description = models.CharField(max_length=999, blank=True)

    def __str__(self):
        return self.name


class TitleMembership(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(blank=True, default=False)
    new = models.BooleanField(blank=True, default=True)


class Border(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="border")
    name = models.CharField(max_length=999, blank=True)
    slug = models.CharField(max_length=999, blank=True)
    description = models.CharField(max_length=999, blank=True)

    def __str__(self):
        return self.name


class BorderMembership(models.Model):
    border = models.ForeignKey(Border, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(blank=True, default=False)
    new = models.BooleanField(blank=True, default=True)


class Achievement(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="achievements", blank=True, null=True)
    name = models.CharField(max_length=999, blank=True)
    slug = models.CharField(max_length=999, blank=True)
    category = models.CharField(max_length=999, blank=True)
    weight = models.IntegerField(default=0, blank=True, null=False)
    description = models.CharField(max_length=999, blank=True)
    game = models.CharField(max_length=999, blank=True)
    active = models.BooleanField(blank=True)

    def __str__(self):
        return self.name


class AchievementMembership(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(blank=True, default=False)
    new = models.BooleanField(blank=True, default=True)


class Preferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publicationNotificationPref = models.BooleanField(default="1")
    userNotificationPref = models.BooleanField(default="1")
    commentNotificationPref = models.BooleanField(default="1")
    forumNotificationPref = models.BooleanField(default="1")


class UserFriendship(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="friends", on_delete=models.CASCADE)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    follow = models.BooleanField(blank=True, default=False)
    block = models.BooleanField(blank=True, default=False)

    class Meta:
        unique_together = ('friend', 'follower')


class TagFollow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followed_tags", on_delete=models.CASCADE)
    tag = models.ForeignKey(CustomTag, related_name="tag_followed", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tag', 'follower')


from API.user.signals.user import *  # noqa isort:skip
