import datetime

from django.db import models


class Conversation(models.Model):
    """
    A user pair chat
    """
    user_1 = models.ForeignKey('user.user', related_name="chat_user_1", on_delete=models.CASCADE)
    user_2 = models.ForeignKey('user.user', related_name="chat_user_2", on_delete=models.CASCADE)
    last_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user_1', 'user_2')

    def __str__(self):
        return str(self.last_timestamp) + " - " + self.user_1.username + " - " + self.user_2.username

    @staticmethod
    def get_last_snippet(conversation_id):
        message = ChatMessage.objects.filter(conversation=conversation_id).order_by("-timestamp").first()
        if message:
            return message.content[-120:]
        else:
            return None

    @staticmethod
    def get_last_timestamp(conversation_id):
        message = ChatMessage.objects.filter(conversation=conversation_id).order_by("-timestamp").first()
        conversation = Conversation.objects.get(id=conversation_id)
        if message:
            conversation.last_timestamp = message.timestamp
        else:
            conversation.last_timestamp = datetime.datetime.now()
        conversation.save()

        return conversation.last_timestamp

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "conversation-%s" % self.user_1.username + "_" + self.user_2.username


class ChatMessage(models.Model):
    """
    A chat message
    """
    conversation = models.ForeignKey(Conversation, related_name="conversation", on_delete=models.CASCADE)
    user = models.ForeignKey('user.user', related_name="chat_message_author", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)
