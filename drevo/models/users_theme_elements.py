from django.db import models
from drevo.models.themes_data import ThemeWork
from users.models import User
from drevo.models import Znanie


class ThemeAdditionalElements(models.Model):
    """
    Таблица для хранения пользовательских элементов темы
    """

    TYPE_CHOICES = [
        ('necessary', 'Состав обязательный'),
        ('unnecessary', 'Состав желательный'),
    ]

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    theme = models.ForeignKey(Znanie, verbose_name='Тема', related_name='changed_theme',
                                  on_delete=models.CASCADE, limit_choices_to={'tz__name': 'Тема'})
    work = models.ForeignKey(ThemeWork, verbose_name='Работа', on_delete=models.CASCADE)
    parent_element = models.ForeignKey(Znanie, verbose_name='Базовое знание', related_name='basic_element',
                                       on_delete=models.CASCADE)
    element_name = models.CharField(max_length=255, verbose_name='Элемент')
    relation_type = models.CharField(max_length=255, verbose_name='Вид связи', choices=TYPE_CHOICES)
    insertion_type = models.BooleanField(default=False, verbose_name='По связи "Далее"?')

    class Meta:
        verbose_name = 'Пользовательский элемент темы'
        verbose_name_plural = 'Пользовательские элементы тем'

    def __str__(self):
        return f'{self.user} - {self.work}'
