# Generated by Django 3.2.4 on 2024-10-28 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drevo', '0144_auto_20241006_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateobject',
            name='template',
            field=models.TextField(blank=True, default='', max_length=2048, verbose_name='Шаблон'),
        ),
    ]
