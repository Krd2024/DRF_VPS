from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import ServerSerializer
from rest_framework import viewsets
from rest_framework import status
from .models import Server


class ServerSerializerSet(viewsets.ModelViewSet):
    """
    ViewSet для выполнения CRUD операций с моделью Server.

    Данный класс предоставляет стандартные действия:
    - Создание нового виртуального сервера.
    - Получение данных о конкретном сервере по его uid.
    - Вывод списка всех серверов с поддержкой фильтрации по заданным параметрам.
    - Изменение статуса сервера (например, перевод в состояния started, blocked, stopped).
    """

    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = Server.objects.all()

        print(self.request.query_params)

        # Фильтрация по CPU (cpu >= значение)
        cpu = self.request.query_params.get("cpu", None)
        if cpu is not None:
            queryset = queryset.filter(cpu__gte=int(cpu))

        # Фильтрация по оперативной памяти (ram >= значение)
        ram = self.request.query_params.get("ram", None)
        if ram is not None:
            queryset = queryset.filter(ram__gte=int(ram))

        # Фильтрация по HDD (hdd >= значение)
        hdd = self.request.query_params.get("hdd", None)
        if hdd is not None:
            queryset = queryset.filter(hdd__gte=int(hdd))

        # Фильтрация по статусу
        status = self.request.query_params.get("status", None)
        print(status, "< ---- status")
        if status is not None:
            queryset = queryset.filter(status__iexact=status)

        return queryset

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

    @extend_schema(
        summary="Возвращает одну запись.",
        description="Возвращает одну запись по ID .",
        request=ServerSerializer,
        responses={200: ServerSerializer},
    )
    def retrieve(self, request, pk=None):
        """Чтение одной записи"""

        # Получаем VPS по ID
        vps = get_object_or_404(Server, pk=pk)
        vps = self.get_object()
        # Сериализуем найденную VPS
        serializer = ServerSerializer(vps)
        # Возвращаем сериализованные данные
        return Response(serializer.data)

    @extend_schema(
        summary="Получить список всех серверов с поддержкой фильтрации",
        description="Возвращает список всех серверов с поддержкой фильтрации по оперативной памяти и SSD.",
        parameters=[
            OpenApiParameter(
                name="ram",
                description="Фильтр по оперативной памяти (>= значение в ГБ)",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="ssd",
                description="Фильтр по SSD (>= значение в ГБ)",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="status",
                description="Фильтр по статусу (started, blocked, stopped) ",
                required=False,
                type=str,
            ),
        ],
        responses={200: ServerSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Обновить статус",
        description="Обновляет статус сервера по ID (в теле запроса).",
        request=ServerSerializer,
        responses={200: ServerSerializer},
    )
    def partial_update(self, request, *args, **kwargs):

        return super().partial_update(request, *args, **kwargs)
