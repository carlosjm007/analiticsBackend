# Generated by Django 2.1.4 on 2018-12-20 06:03

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ubereats', '0004_urls'),
    ]

    operations = [
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
                ('tipo_comida', models.TextField(blank=True, null=True)),
                ('ubicacion_lista', models.IntegerField(blank=True, null=True)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ubereats.PaginaCiudad')),
            ],
            options={
                'verbose_name': 'Tienda',
                'verbose_name_plural': 'Tiendas',
            },
        ),
    ]