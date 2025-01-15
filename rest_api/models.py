import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Server(models.Model):

    cpu = models.PositiveIntegerField(
        verbose_name="Количество ядер CPU",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(128),
        ],
    )
    ram = models.PositiveIntegerField(
        verbose_name="Объем RAM (ГБ)",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1024),
        ],
    )
    hdd = models.PositiveIntegerField(
        verbose_name="Объем HDD (ГБ)",
        validators=[
            MinValueValidator(10),  # Минимум 10 ГБ
            MaxValueValidator(10240),  # Максимум 10240 ГБ (10 ТБ)
        ],
    )

    STATUS_CHOICES = [
        ("started", "Запущен"),
        ("blocked", "Заблокирован"),
        ("stopped", "Остановлен"),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="stopped",
        verbose_name="Статус сервера",
    )

    def __str__(self):
        return f"Сервер {self.uid}, Статус: {self.status}"

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Серверы"
