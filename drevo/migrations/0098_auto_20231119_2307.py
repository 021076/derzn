# Generated by Django 3.2.4 on 2023-11-19 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drevo', '0097_delete_suggestiontypeclone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='glossaryterm',
            options={'ordering': ('order',), 'verbose_name': 'Термин глоссария', 'verbose_name_plural': 'Термины глоссария'},
        ),
        migrations.CreateModel(
            name='Var',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('knowledge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drevo.znanie', verbose_name='Знание')),
            ],
            options={
                'verbose_name': 'Переменная',
                'verbose_name_plural': 'Переменные',
            },
        ),
    ]
