# Generated by Django 3.2.4 on 2022-12-10 03:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drevo', '0033_auto_20221206_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время решения')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_in_quiz', to='drevo.znanie', verbose_name='Ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_in_quiz', to='drevo.znanie', verbose_name='Вопрос')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passed_quiz', to='drevo.znanie', verbose_name='Тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_results', to=settings.AUTH_USER_MODEL, verbose_name='Тестируемый')),
            ],
            options={
                'verbose_name': 'Результаты теста',
                'verbose_name_plural': 'Результаты тестов',
            },
        ),
    ]
