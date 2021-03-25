from django.shortcuts import render
from rest_framework import viewsets, serializers
from strugglebusapi.models import Tasks
# Create your views here.


class TasksSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    Arguments:
        serializer type
    """
    class Meta:
        model = Tasks
        fields = ('id', 'name', 'completed')
        depth = 1


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
