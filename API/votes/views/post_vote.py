from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.votes.models.post_vote import PostVote, PublicationVote
from API.votes.serializers.post_vote import (PostVoteSerializer,
                                             PostVoteSerializerCreate,
                                             PostVoteSerializerUpdate)
from API.votes.serializers.publication_vote import (
    PublicationVoteSerializer, PublicationVoteSerializerCreate,
    PublicationVoteSerializerUpdate)


# post_votes
class PostVoteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Create post vote
        """
        serializer = PostVoteSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serialized_vote = PostVoteSerializer(serializer.instance).data
            serialized_vote["status"] = "Success"
            return Response(serialized_vote, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post_votes/{post_vote_id}
class PostVoteDetail(APIView):
    @staticmethod
    def patch(request, post_vote_id):
        """
        Update post vote
        """

        post_vote = get_object_or_404(PostVote, pk=post_vote_id)
        serializer = PostVoteSerializerUpdate(post_vote, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PostVoteSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, post_vote_id):
        """
        Delete post vote
        """

        post_vote = get_object_or_404(PostVote, pk=post_vote_id)
        if post_vote.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post_vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# publication_votes
class PublicationVoteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Create publication vote
        """

        serializer = PublicationVoteSerializerCreate(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(PublicationVoteSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# publication_votes/{publication_vote_id}
class PublicationVoteDetail(APIView):
    @staticmethod
    def patch(request, publication_vote_id):
        """
        Update publication vote
        """

        publication_vote = get_object_or_404(PublicationVote,
                                             pk=publication_vote_id
                                             )
        serializer = PublicationVoteSerializerUpdate(publication_vote,
                                                     data=request.data,
                                                     context={'request': request},
                                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PublicationVoteSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, publication_vote_id):
        """
        Delete publication vote
        """

        publication_vote = get_object_or_404(PublicationVote, pk=publication_vote_id)
        if publication_vote.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        publication_vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
