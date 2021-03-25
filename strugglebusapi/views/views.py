from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework import viewsets, serializers, status
from strugglebusapi.models import Tasks
from rest_framework.response import Response
# Create your views here.


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'name', 'completed')
        depth = 1


class TasksViewSet(viewsets.ViewSet):
    # queryset = Tasks.objects.all()
    # serializer_class = TasksSerializer

    def list(self, request):
        tasks = Tasks.objects.all()
        tasks = TasksSerializer(tasks, many=True, context={'request': request})

        return Response(tasks.data)

    def destroy(self, request, pk=None):
        try:
            task = Tasks.objects.get(pk=pk)
            task.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Tasks.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        task = Tasks.objects.get(pk=pk)
        task.name = request.data['name']
        try:
            task.save()
            task = TasksSerializer(task, many=False, context={
                                   'request': request})
            return Response(task.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        task = Tasks()
        task.name = request.data['name']
        task.completed = request.data['completed']
        try:
            task.save()
            serializer = TasksSerializer(task, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
