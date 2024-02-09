from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import ToDo, User, Status
from app.serializers import ToDoSerializer
from datetime import date


@api_view(['GET'])
def get_list_todo(request, format=None):
    """
    Возвращает список дел по запросу
    """
    todos = ToDo.objects.all()
    serializer = ToDoSerializer(todos, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_todo(request, format=None):
    """
    Добавляет дело по запросу
    """
    todo = ToDo.objects.create(
        text = request.data.get('text'),
        user_id = User.objects.get(id=2),
        status_id = Status.objects.get(id=1),
        date_completion = date.today()
    )
    todo.save()
    serializer = ToDoSerializer(todo)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_todo(request, id, format=None):
    """
    Удаляет дело по запросу
    """
    todo = get_object_or_404(ToDo, id=id)
    todo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def put_status_todo(request, id, format=None):
    """
    Обновляет статус дела по запросу
    """
    todo = get_object_or_404(ToDo, id=id)
    todo.status_id = Status.objects.get(id=2)
    todo.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
def put_text_todo(request, id, format=None):
    """
    Обновляет текст дела по запросу
    """
    todo = get_object_or_404(ToDo, id=id)
    todo.text = request.data.get('text')
    todo.save()
    return Response(status=status.HTTP_200_OK)