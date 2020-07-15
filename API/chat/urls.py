from django.conf.urls import url

from API.chat.views.chat import ChatMessageView, ConversationView

urlpatterns = [
    # Posts
    url(r'^chat/$', ConversationView.as_view()),
    url(r'^chat/(?P<chat_id>[\w-]+)$', ChatMessageView.as_view()),
]
