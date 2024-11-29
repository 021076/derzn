from django.db import models

from drevo.models.courses_data import CourseWork
from users.models import User
from drevo.models import Znanie


class CourseAdditionalElements(models.Model):
    """
    Таблица для хранения пользовательских элементов обучения
    """

    TYPE_CHOICES = [
        ('necessary', 'Состав обязательный'),
        ('unnecessary', 'Состав желательный'),
    ]

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    course = models.ForeignKey(Znanie, verbose_name='Курс', related_name='changed_course',
                                  on_delete=models.CASCADE, limit_choices_to={'tz__name': 'Курс'})
    work = models.ForeignKey(CourseWork, verbose_name='Работа', on_delete=models.CASCADE)
    parent_element = models.ForeignKey(Znanie, verbose_name='Базовое знание', related_name='basic_know',
                                       on_delete=models.CASCADE)
    element_name = models.CharField(max_length=255, verbose_name='Элемент')
    relation_type = models.CharField(max_length=255, verbose_name='Вид связи', choices=TYPE_CHOICES)
    insertion_type = models.BooleanField(default=False, verbose_name='По связи "Далее"?')

    class Meta:
        verbose_name = 'Пользовательский элемент курса'
        verbose_name_plural = 'Пользовательские элементы курсов'

    def __str__(self):
        return f'{self.user} - {self.work}'
