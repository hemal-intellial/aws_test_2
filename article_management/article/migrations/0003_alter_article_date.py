# Generated by Django 3.2.12 on 2022-02-18 09:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20220218_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 18, 15, 27, 27, 64173)),
        ),
    ]
