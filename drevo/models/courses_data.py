from django.db import models
from users.models import User
from drevo.models import Znanie


class CourseWork(models.Model):
    """
    Таблица для хранения работ по курсу
    """
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    course = models.ForeignKey(Znanie, verbose_name='Курс', on_delete=models.CASCADE, limit_choices_to={'tz__name':'Курс'})
    work_name = models.CharField(max_length=255, verbose_name='Работа')

    class Meta:
        verbose_name = 'Работа по курсу'
        verbose_name_plural = 'Работы по курсам'

    def __str__(self):
        return f'{self.user} - {self.work_name}'


class CourseData(models.Model):
    """
    Таблица для хранения данных курсов
    """

    TYPE_CHOICES = [
        ('active', 'Активный'),
        ('completed', 'Завершенный'),
        ('available', 'Доступный'),
    ]

    course = models.ForeignKey(Znanie, verbose_name='Курс', related_name='passed_course',
                                  on_delete=models.CASCADE, limit_choices_to={'tz__name': 'Курс'})
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    element = models.CharField(max_length=255, verbose_name='Элемент')
    element_type = models.CharField(max_length=255, verbose_name='Тип элемента', choices=TYPE_CHOICES)
    work = models.ForeignKey(CourseWork, verbose_name='Работа', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Данные курса'
        verbose_name_plural = 'Данные курсов'

    def __str__(self):
        return f'{self.user} - {self.work}'
