from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    def get(self, request, format=None):
        # Queryset to get all notifications for the authenticated user
        queryset = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)


class NotificationMarkAsReadView(APIView):
    def post(self, request, format=None):
        # Mark all notifications as read for the authenticated user
        Notification.objects.filter(user=request.user).update(read=True)
        return Response({'message': 'All notifications marked as read.'})


class NotificationMarkSingleAsReadView(APIView):
    def post(self, request, notification_id, format=None):
        # Mark a single notification as read for the authenticated user
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.read = True
            notification.save()
            return Response({'message': 'Notification marked as read.'})
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found.'}, status=404)