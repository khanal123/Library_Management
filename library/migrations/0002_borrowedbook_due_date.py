# Generated by Django 5.0.2 on 2024-03-07 07:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowedbook',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 7, 11, 35, 965297, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
