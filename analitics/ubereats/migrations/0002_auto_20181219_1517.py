# Generated by Django 2.1.4 on 2018-12-19 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ubereats', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productos',
            name='tienda',
        ),
        migrations.RemoveField(
            model_name='tienda',
            name='ciudad',
        ),
        migrations.RemoveField(
            model_name='url',
            name='ciudad',
        ),
        migrations.DeleteModel(
            name='Productos',
        ),
        migrations.DeleteModel(
            name='Tienda',
        ),
        migrations.DeleteModel(
            name='Url',
        ),
    ]
