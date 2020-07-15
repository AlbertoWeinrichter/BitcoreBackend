from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.user.serializers.social import (TagFollowSerializerCreate,
                                         UserFriendshipSerializerCreate)


class FollowUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Follow a user and get a notification when he publishes something
        {
        'followed': username of user to be followed (required)
        'follow': boolean
        'block': boolean
            ->Either follow or block should be sent
        }
        """
        serializer = UserFriendshipSerializerCreate(
            data=request.data,
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowTag(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Follow a tag so a notification is sent when content with this tag gets published
        {
        'tag': slug of tag to be followed (required)
        }
        """
        serializer = TagFollowSerializerCreate(
            data=request.data,
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchAutocomplete(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        User search autocomplete helper method
        {
        'string': string of characters to search a user by
        }
        """
        serializer = TagFollowSerializerCreate(
            data=request.data,
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
