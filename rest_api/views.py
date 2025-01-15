import uuid
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.response import Response
from .serializers import ServerSerializer
from .models import Server
from rest_framework import viewsets
from rest_framework import status


class ServerSerializerSet(viewsets.ViewSet):
    """
    ViewSet для выполнения CRUD операций с моделью Server.

    Данный класс предоставляет стандартные действия:
    - Создание нового виртуального сервера.
    - Получение данных о конкретном сервере по его uid.
    - Вывод списка всех серверов с поддержкой фильтрации по заданным параметрам.
    - Изменение статуса сервера (например, перевод в состояния started, blocked, stopped).
    """

    queryset = Server.objects.all()

    @extend_schema(
        summary="Создаёт VPS",
        description="Создание нового VPS",
        request=ServerSerializer,
        responses={
            201: ServerSerializer,
        },
    )
    def create(self, request):
        """Создать VPS"""

        # Создаем экземпляр сериализатора с данными из запроса
        serializer = ServerSerializer(data=request.data)

        # Проверяем, валидны ли переданные данные
        if serializer.is_valid():
            # Если данные валидны, сохраняем новуй VPS в базе данных
            serializer.save()

            # Возвращаем сериализованные данные задачи с HTTP статусом 201 (Created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Если данные не валидны, возвращаем ошибки сериализатора с HTTP статусом 400 (Bad Request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
