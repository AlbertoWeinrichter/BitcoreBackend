from django.conf.urls import url

from API.notifications.views.notification import NotificationView

urlpatterns = [
    # Notifications
    url(r'^notifications$', NotificationView.as_view()),
]
