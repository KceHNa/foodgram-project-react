# Generated by Django 3.2 on 2022-08-18 14:20

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220818_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFFFF', image_field=None, max_length=18, samples=None, unique=True, verbose_name='Цвет'),
        ),
    ]
