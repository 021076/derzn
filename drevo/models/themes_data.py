from django.db import models
from users.models import User
from drevo.models import Znanie


class ThemeWork(models.Model):
    """
    Таблица для хранения работ по теме
    """
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    theme = models.ForeignKey(Znanie, verbose_name='Тема', on_delete=models.CASCADE, limit_choices_to={'tz__name':'Тема'})
    work_name = models.CharField(max_length=255, verbose_name='Работа')

    class Meta:
        verbose_name = 'Работа по теме'
        verbose_name_plural = 'Работы по темам'

    def __str__(self):
        return f'{self.user} - {self.work_name}'


class ThemeData(models.Model):
    """
    Таблица для хранения данных тем
    """

    TYPE_CHOICES = [
        ('active', 'Активный'),
        ('completed', 'Завершенный'),
        ('available', 'Доступный'),
    ]

    theme = models.ForeignKey(Znanie, verbose_name='Тема', related_name='passed_theme',
                                  on_delete=models.CASCADE, limit_choices_to={'tz__name': 'Тема'})
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    element = models.CharField(max_length=255, verbose_name='Элемент')
    element_type = models.CharField(max_length=255, verbose_name='Тип элемента', choices=TYPE_CHOICES)
    work = models.ForeignKey(ThemeWork, verbose_name='Работа', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Данные темы'
        verbose_name_plural = 'Данные тем'

    def __str__(self):
        return f'{self.user} - {self.work}'
