from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.chat.models.chat import ChatMessage, Conversation
from API.chat.serializers.chat import (ChatConversationCreateSerializer,
                                       ChatMessageCreateSerializer,
                                       ChatMessageSerializer,
                                       ConversationSerializer)


class ConversationView(APIView):
    permission_classes = ()

    @staticmethod
    def get(request):
        """
        Get conversations
        """
        conversations = Conversation.objects.filter(
            Q(user_1=request.user) | Q(user_2=request.user)
        )
        serialized_conversations = ConversationSerializer(conversations, context={'request': request}, many=True).data
        # orderedConversations = [{c["id"]: c} for c in serialized_conversations][:10]
        return Response({"conversations": serialized_conversations})

    @staticmethod
    def post(request):
        """
        Create chat conversation

        username(required) - user to start conversation with
        """

        serializer = ChatConversationCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            conversation = serializer.save()
            if conversation:
                return Response(ConversationSerializer(conversation, context={'request': request}).data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response("Already exists", status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatMessageView(APIView):
    permission_classes = ()

    @staticmethod
    def get(request, chat_id):
        """
        Get messages of conversation
        """
        messages = reversed(ChatMessage.objects.filter(conversation=chat_id).order_by("-timestamp")[:5])
        serialized_messages = ChatMessageSerializer(messages, many=True).data

        return Response(serialized_messages)

    @staticmethod
    def post(request, chat_id):
        """
        Create chat message

        content(required) - content of the message \n
        conversation_id(required) - id of target conversation \n
        """

        serializer = ChatMessageCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
