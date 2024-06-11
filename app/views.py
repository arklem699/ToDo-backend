from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import ToDo, User, Status
from app.serializers import ToDoSerializer, UserSerializer
from datetime import date


@api_view(['POST'])
def registration(request, format=None):
    """
    Регистрация пользователя
    """
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user) # Создание Refesh и Access
        refresh.payload.update({    # Полезная информация в самом токене
            'user_id': user.id,
            'username': user.username
        })

        return Response({                       # Отправка на клиент
                'refresh': str(refresh),
                'access': str(refresh.access_token), 
            }, status=status.HTTP_201_CREATED)
    
    return Response({'error': 'Неверные данные'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request, format=None):
    """
    Аутентификация пользователя
    """
    User = get_user_model()

    data = request.data
    email = data.get('email', None)
    password = data.get('password', None)
    if email is None or password is None:
        return Response({'error': 'Введите почту и пароль'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(email=email).first()
    if user is None or not user.check_password(password):
        return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    refresh.payload.update({
        'user_id': user.id,
        'username': user.username
    })

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'username': user.username,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout(request, format=None):
    """
    Выход из профиля
    """
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'Необходим Refresh token'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist() # Добавить токен в чёрный список

    except Exception:
        return Response({'error': 'Неверный Refresh token'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)


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