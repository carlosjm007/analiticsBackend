# Generated by Django 2.1.4 on 2019-01-29 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubereats', '0018_paginaciudad_actualizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='urls',
            name='mapeado',
            field=models.BooleanField(default=True),
        ),
    ]
