from django.db import models

from campaigns.models import Campaign


class Lead(models.Model):
    """Модель потенциального клиента"""
    class Meta:
        verbose_name = 'Потенциальный клиент'
        verbose_name_plural = 'Потенциальные клиенты'

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    telephone  = models.CharField(max_length=50, default=0, verbose_name='Телефон')
    email = models.EmailField(max_length=50, default='', verbose_name='Email')
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='leads'
    )

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
