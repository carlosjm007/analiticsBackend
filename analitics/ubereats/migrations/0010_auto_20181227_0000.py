# Generated by Django 2.1.4 on 2018-12-27 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubereats', '0009_dayweek_hourday_productobusqueda_tiendabusqueda'),
    ]

    operations = [
        migrations.AddField(
            model_name='paginaciudad',
            name='timezone',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='productobusqueda',
            name='editado',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='tiendabusqueda',
            name='editado',
            field=models.DateField(auto_now=True),
        ),
    ]