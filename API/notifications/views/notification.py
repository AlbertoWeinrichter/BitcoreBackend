from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.notifications.models.notification import Notification
from API.notifications.serializers.notification import NotificationSerializer


class NotificationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request):
        """
        List notifications
        """

        notifications = Notification.objects.filter(owner_id=request.user.id, new=True)[:5]
        if len(notifications) > 0:
            return Response(NotificationSerializer(notifications, many=True).data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def post(request):
        try:
            notifications = Notification.objects.filter(id__in=request.data["notifications"])
            for n in notifications:
                n.new = False
                n.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
