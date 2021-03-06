# Generated by Django 2.1.4 on 2018-12-19 00:19

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_remove_ciudad_url_pagina'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('uuid', models.CharField(max_length=50)),
                ('latitud', models.FloatField(default=0.0)),
                ('longitud', models.FloatField(default=0.0)),
                ('calificacion', models.DecimalField(decimal_places=1, default=Decimal('0.0'), max_digits=3)),
                ('disponible', models.BooleanField(default=True)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Ciudad')),
            ],
            options={
                'verbose_name': 'Tienda',
                'verbose_name_plural': 'Tiendas',
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('primera', models.BooleanField(default=False)),
                ('offset', models.CharField(blank=True, max_length=15, null=True)),
                ('pageSize', models.CharField(blank=True, max_length=15, null=True)),
                ('request_payload', models.CharField(max_length=1000)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Ciudad')),
            ],
            options={
                'verbose_name': 'URL',
                'verbose_name_plural': 'URLs',
            },
        ),
        migrations.AddField(
            model_name='productos',
            name='tienda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ubereats.Tienda'),
        ),
    ]
