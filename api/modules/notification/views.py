from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Notification, NotificationTypeChoice
from api.modules.notification.serializers import NotificationSerializer


def add_notification(initiator_user, destined_user, text, notification_type=NotificationTypeChoice.COMMON.value):
    """
    Add Notification for user
    :param request:
    :param initiator_user:
    :param destined_user:
    :param text:
    :param notification_type:
    :return: True if notification created
    :return: False if error occurs
    """
    try:
        Notification.objects.create(
            initiator_user=initiator_user,
            destined_user=destined_user,
            text=text,
            notification_type=notification_type,
        )
    except Exception:
        return False  # Failed to create notification
    return True  # Notification successfully Created


@api_view(['GET'])
def get_notifications(request):
    """
    Display all notification for request user
    :param request:
    :return: 200 successful
    """
    notifications = Notification.objects.filter(destined_user=request.user).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def mark_notification_as_read(request, notification_id):
    """
    Mark notification as read
    :param request:
    :param notification_id:
    :return 200 successful
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        if request.user != notification.destined_user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        notification.is_read = True
        notification.save()

    except Notification.DoesNotExist:
        error_message = "Notification does not exist"
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)

    success_message = "Successfully marked notification as read."
    return Response(success_message, status=status.HTTP_200_OK)


@api_view(['GET'])
def mark_all_notification_as_read(request):
    """
    Mark all notification as read
    :param request:
    :return 200 successful
    """
    notifications = Notification.objects.filter(destined_user=request.user)
    notifications.update(is_read=True)
    success_message = "Successfully marked all notifications as read."
    return Response(success_message, status=status.HTTP_200_OK)
