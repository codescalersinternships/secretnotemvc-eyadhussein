# Generated by Django 5.0.7 on 2024-07-16 22:22

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('expiration_date', models.DateTimeField(default=datetime.datetime(2024, 8, 15, 22, 22, 24, 879168, tzinfo=datetime.timezone.utc), verbose_name='expiration_date')),
                ('current_views', models.IntegerField(default=0)),
                ('max_views', models.IntegerField(default=1)),
            ],
        ),
    ]
