from django.db import models

from services.models import Service


class Campaign(models.Model):
    """Модель рекламной компании"""

    CHANNEL_CHOICES: list = [
        ('vk', 'ВКонтакте'),
        ('ig', 'Instagram'),
        ('tg', 'Telegram'),
        ('yandex', 'Яндекс.Директ'),
        ('google', 'Google Ads'),
        ('other', 'Другое'),
    ]

    class Meta:
        verbose_name = 'Рекламная компания'
        verbose_name_plural = 'Рекламные компании'

    name = models.CharField(max_length=200, verbose_name='Название')
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='campaigns',
        verbose_name='Рекламируемая услуга'
    )
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, verbose_name='Канал продвижения')
    budget = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='Бюджет')

    def get_roi(self) -> float | None:
        if hasattr(self, 'total_income') and self.total_income is not None and self.budget:
            return round((self.total_income - self.budget) / self.budget * 100, 1)
        return None

    def __str__(self) -> str:
        return self.name
