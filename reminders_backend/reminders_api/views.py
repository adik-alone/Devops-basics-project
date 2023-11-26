from .serializers import ReminderSerializer
from .models import Reminder
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status


class ReminderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # return list of actual reminders, created by current user
        queryset = Reminder.objects.filter(creator=request.user, is_done=False)
        serializer = ReminderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        # return reminder by it's id
        queryset = Reminder.objects.all()
        reminder = get_object_or_404(queryset, pk=pk)
        if reminder.creator != request.user:
            return Response({
                "Error": "You dont have access to this reminder"
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = ReminderSerializer(reminder)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        # update reminder fields
        queryset = Reminder.objects.all()
        reminder = get_object_or_404(queryset, pk=pk)
        serializer = ReminderSerializer(reminder, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.user != reminder.creator:
            return Response({
                "Error": "You dont have access to this reminder"
            }, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # create reminder field
        serializer = ReminderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        # change is_done flag to true
        queryset = Reminder.objects.all()
        reminder = get_object_or_404(queryset, pk=pk)
        if request.user != reminder.creator:
            return Response({
                "Error": "You dont have access to this reminder"
            }, status=status.HTTP_403_FORBIDDEN)
        reminder.is_done = True
        reminder.save()
        return Response({"Reminder successfully done"}, status=status.HTTP_204_NO_CONTENT)
