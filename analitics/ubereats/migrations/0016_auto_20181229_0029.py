# Generated by Django 2.1.4 on 2018-12-29 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubereats', '0015_tienda_last_trend'),
    ]

    operations = [
        migrations.AddField(
            model_name='paginaciudad',
            name='lat1',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='paginaciudad',
            name='lat2',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='paginaciudad',
            name='lng1',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='paginaciudad',
            name='lng2',
            field=models.FloatField(default=0.0),
        ),
    ]
