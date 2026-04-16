from django.db import models

from contracts.models import Contract
from leads.models import Lead


class Customer(models.Model):
    """Модель клиента"""
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    lead = models.OneToOneField(
        Lead,
        on_delete=models.PROTECT,
        related_name='customer',
        verbose_name='Потенциальный клиент'
    )
    contract = models.ForeignKey(
        Contract,
        on_delete=models.PROTECT,
        related_name='active_clients',
        verbose_name='Контракт'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата активации')

    def __str__(self) -> str:
        return f"{self.lead.last_name} {self.lead.first_name}"
