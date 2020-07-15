import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers

from API.chat.models.chat import ChatMessage, Conversation
from API.user.models.user import User


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"

    def to_representation(self, instance):
        data = super(ConversationSerializer, self).to_representation(instance)
        if self.context["request"].user.username == instance.user_1.username:
            user_to_show = instance.user_2
        else:
            user_to_show = instance.user_1

        messages = reversed(ChatMessage.objects.filter(conversation=instance.id).order_by("-timestamp")[:10])
        serialized_messages = ChatMessageSerializer(messages, many=True).data
        data.update({
            'username': user_to_show.username,
            'avatar': user_to_show.avatar_cropped,
            'last_snippet': instance.get_last_snippet(instance.id),
            'last_timestamp': instance.get_last_timestamp(instance.id),
            'messages': serialized_messages
        })

        return data


class ChatConversationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ""

    def save(self):
        other_user = User.objects.get(username=self.context["request"].data["username"])
        owner = self.context["request"].user

        conversation, created = Conversation.objects.get_or_create(
            user_1=owner,
            user_2=other_user,
        )
        if created:
            conversation.last_timestamp = datetime.datetime.now()
            conversation.save()
            return conversation
        else:
            return False

    def to_representation(self, instance):
        data = super(ChatConversationCreateSerializer, self).to_representation(instance)

        return data


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        exclude = ("user", "id",)

    def to_representation(self, instance):
        data = super(ChatMessageSerializer, self).to_representation(instance)
        username = instance.user.username
        data.update({
            'username': username
        })

        return data


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ""

    def save(self):
        conversation = Conversation.objects.get(id=self.context["request"].data["conversationId"])
        user = self.context["request"].user

        if user.username == conversation.user_1.username:
            user_to_send = conversation.user_2.username
        else:
            user_to_send = conversation.user_1.username

        # Create message object and serialize it to be sent over websocket
        m = ChatMessage.objects.create(
            user=user,
            conversation=conversation,
            content=self.context["request"].data["message"]
        )
        message_data = ChatMessageSerializer(m).data

        # Send to appropiate user channel
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            user_to_send,
            {"type": "chat.message",
             "data": message_data},
        )
