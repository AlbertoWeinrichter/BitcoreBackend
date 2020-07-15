import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from haystack.query import SearchQuerySet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.general.models.general import CustomTag
from API.notifications.models.notification import Notification
from API.notifications.serializers.notification import NotificationSerializer
from API.user.models.user import (Achievement, AchievementMembership, Border,
                                  BorderMembership, TagFollow, Title,
                                  TitleMembership, User, UserFriendship)
from API.user.serializers.social import TagFollowSerializer
from API.user.serializers.user import (AchievementTrueSerializer,
                                       CompleteUserSerializer,
                                       ProfileUserSerializer,
                                       TitleTrueSerializer,
                                       UserFriendshipSerializer)
from API.utils import constants

logger = logging.getLogger(__name__)


class UserAutocomplete(APIView):
    permission_classes = ()

    def get(self, request):
        search_string = request.query_params.get('user_search', None)

        if search_string:
            sqs = SearchQuerySet().models(User).autocomplete(username_auto=search_string)
            suggestions = [{"username": result.username} for result in sqs[:5]]
        else:
            suggestions = []

        return Response({"results": suggestions})


class SubscriptionView(APIView):
    permission_classes = ()

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, username):
        """
        Get followed and blocked users and tags
        """
        user = get_object_or_404(User, username=username)

        friendships = UserFriendship.objects.filter(follower=user, follow=True)
        serialized_friends = UserFriendshipSerializer(friendships, many=True).data

        blocked = UserFriendship.objects.filter(follower=user, block=True)
        serialized_blocked = UserFriendshipSerializer(blocked, many=True).data

        followers = UserFriendship.objects.filter(friend=user, follow=True)
        serialized_followers = UserFriendshipSerializer(followers, many=True).data

        followed_tags = TagFollow.objects.filter(follower=user)
        serialized_tags = TagFollowSerializer(followed_tags, many=True).data

        response = {
            "friendships": serialized_friends,
            "followers": serialized_followers,
            "blocked": serialized_blocked,
            "followed_tags": serialized_tags
        }

        return Response(response, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Update avatar S3 url, avatar coordinates, follow or unfollow a tag, email or username, achievement,
        frame or title for authenticated user
        """

        data = request.data.get('data')
        try:
            allowed = ["username", "email", "avatar", "avatar_cropped"]
            for k, v in data.items():
                if k in allowed:
                    request.user.__setattr__(k, v)

                elif k == "tag_follow" and isinstance(data.get("tag_follow"), list):
                    for t in data.get("tag_follow"):
                        sender = request.user
                        tag = CustomTag.objects.get(slug=t.get("slug"))
                        tag_follow, created = TagFollow.objects.get_or_create(
                            follower=sender,
                            tag=tag
                        )
                        tag_follow.follow = t.get("follow")

                        tag_follow.save()

                elif k == "friendship" and isinstance(data.get("friendship"), list):
                    for f in data.get("friendship"):
                        sender = request.user
                        receiver = User.objects.get(username=f.get("username"))
                        friendship, created = UserFriendship.objects.get_or_create(
                            follower=sender,
                            followed=receiver
                        )
                        if f.get("follow"):
                            friendship.follow = f.get("follow")
                        if f.get("block"):
                            friendship.block = f.get("block")

                        friendship.save()

                elif k == "active_title" and isinstance(data.get("active_title"), str):
                    try:
                        old_title = TitleMembership.objects.filter(user=request.user, active="1").first()
                        if old_title:
                            old_title.active = "0"
                            old_title.save()
                        new_title = TitleMembership.objects.get(
                            user=request.user,
                            title=Title.objects.get(name=data.get("active_title"))
                        )
                        if new_title:
                            new_title.active = "1"
                            new_title.save()
                    except Exception as e:
                        logger.error(e)
                        return Response({constants.ERROR: "You can't pick titles you don't own"})

                elif k == "active_border" and isinstance(data.get("active_border"), str):
                    try:
                        old_border = BorderMembership.objects.filter(user=request.user, active="1").first()
                        if old_border:
                            old_border.active = "0"
                            old_border.save()
                        new_border = BorderMembership.objects.get(
                            user=request.user,
                            border=Border.objects.get(slug=data.get("active_border"))
                        )
                        if new_border:
                            new_border.active = "1"
                            new_border.save()
                    except Exception as e:
                        logger.error(e)
                        return Response({constants.ERROR: "You can't pick borders you don't own"})

                elif k == "active_achievements" and isinstance(data.get("active_achievements"), list) and len(
                        data.get("active_achievements")) < 4:  # noqa conflict with flake8 E125
                    try:
                        if len(data.get("active_achievements")) == 3:
                            channel_layer = get_channel_layer()

                            # Waka Waka Waka
                            # Select 3 achievements for the first time
                            waka_waka_waka, created = AchievementMembership.objects.get_or_create(
                                user=request.user,
                                achievement=Achievement.objects.get(slug="waka_waka_waka")
                            )
                            if created:
                                notification = Notification.objects.create(
                                    notification_type="achievement",
                                    owner=request.user,
                                    new_achievement=waka_waka_waka,
                                    notification_message=waka_waka_waka.achievement.name
                                )
                                serialized_notification = NotificationSerializer(notification).data
                                async_to_sync(channel_layer.group_send)(
                                    slugify(user_to_send.username),  # TODO: WTF? Fix this
                                    {"type": "message",
                                     "data": serialized_notification},
                                )

                        old_achievements = AchievementMembership.objects.filter(user=request.user, active="1")
                        if len(old_achievements) > 0:
                            for a in old_achievements:
                                a.active = False
                                a.save()

                        for a in data.get("active_achievements"):
                            new_achievement = AchievementMembership.objects.get(
                                user=request.user,
                                achievement=Achievement.objects.get(slug=a)
                            )
                            new_achievement.active = True
                            new_achievement.save()
                    except Exception as e:
                        logger.error(e)
                        return Response({constants.ERROR: "You can't pick achievements you don't own"})

                else:
                    return Response({status.HTTP_400_BAD_REQUEST: "Nothing to update or error sending user data"})

            request.user.save()
            serialized_user = CompleteUserSerializer(request.user).data
            return Response(serialized_user)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdatePreferences(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Update preferences for authenticated user
        """
        data = request.data.get('data')
        try:
            allowed = [
                "PublicationNotificationPref",
                "UserNotificationPref",
                "CommentNotificationPref",
                "ForumNotificationPref"]
            for k, v in data.items():
                if k in allowed:
                    request.user.__setattr__(k, v)

            request.user.save()
            return Response({constants.SUCCESS: 'User has been updated'})
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Login a user user
        """
        user = request.user
        return Response(CompleteUserSerializer(user).data)


class UserTutorial(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        Endpoint for tutorial interaction
        Update username and avatar
        Set new_user = False when tutorial is over or skipped
        """
        try:
            allowed = ["username", "avatar", "avatar_cropped"]

            for k, v in request.data.items():
                if k in allowed and len(v) > 2:
                    request.user.__setattr__(k, v)
            request.user.save()
            request.user.new_user = False
            request.user.save()

            user = get_object_or_404(User, username=request.user.username)
            serialized_user = CompleteUserSerializer(user).data
            return Response(serialized_user)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            user = request.user
            user.new_user = False
            user.save()
            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, username):
        """
        View individual user
        """
        user = get_object_or_404(User, username=username)
        serialized_user = CompleteUserSerializer(user).data
        return Response(serialized_user)

    @staticmethod
    def delete(request, user_id):
        """
        Delete user
        """
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewUsersView(APIView):
    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        """
        Get list of user profiles with highests scores
        """

        users = User.objects.all().order_by("-date_joined")[:5]
        serialized_users = ProfileUserSerializer(users, many=True).data
        return Response({"users": serialized_users})


class AchievementList(APIView):
    permission_classes = ()

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        achievements = Achievement.objects.all()
        titles = Title.objects.all()

        user_item_list = {}
        user_item_list.update({"achievements": AchievementTrueSerializer(achievements, many=True).data})
        user_item_list.update({"titles": TitleTrueSerializer(titles, many=True).data})

        return Response(user_item_list)
