from django.db import models

class Service(models.Model):
    """Модель услуги"""
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    name = models.CharField(max_length=200, verbose_name='Название')
    description  = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Стоимость')

    def __str__(self):
        return self.name