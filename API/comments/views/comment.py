from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.comments.models.comment import Comment
from API.comments.serializers.comment import (CommentSerializerCreate,
                                              CommentSerializerUpdate,
                                              CommentTreeSerializer)
from API.publication.models.publication import Publication


class LoadComment(APIView):
    permission_classes = ()

    @staticmethod
    def get(request, slug):
        publication = Publication.objects.get(slug=slug)
        comments = Comment.objects.filter(publication=publication.id, parent=None).order_by('-timestamp')
        total = len(Comment.objects.filter(publication=publication))

        response = CommentTreeSerializer(comments, context={'request': request}, many=True).data

        return Response({
            'comments': response,
            'total': total
        })


class CreateComment(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Create comment

        body(required) - content of the message \n
        publication(required) - id of target publication \n
        """

        serializer = CommentSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditComment(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def patch(request, comment_id):
        """
        Update comment
        """

        post = get_object_or_404(Comment, pk=comment_id)
        serializer = CommentSerializerUpdate(post, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, post_id):
        """
        Delete post
        """

        comment = get_object_or_404(Comment, pk=post_id)
        if comment.user != request.user:
            return Response({"status": "Error: You can't delete other users comments"},
                            status=status.HTTP_401_UNAUTHORIZED)
        comment.delete()
        return Response({"status": "Success"}, status=status.HTTP_204_NO_CONTENT)
