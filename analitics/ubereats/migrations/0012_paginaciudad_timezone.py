# Generated by Django 2.1.4 on 2018-12-27 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubereats', '0011_remove_paginaciudad_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='paginaciudad',
            name='timezone',
            field=models.CharField(default='0', max_length=3),
        ),
    ]
