# Generated by Django 2.1.4 on 2018-12-23 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubereats', '0007_tienda_nombre_google'),
    ]

    operations = [
        migrations.AddField(
            model_name='tienda',
            name='direccion_google',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
