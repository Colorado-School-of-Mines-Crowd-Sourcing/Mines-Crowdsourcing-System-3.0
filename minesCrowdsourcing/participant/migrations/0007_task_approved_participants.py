# Generated by Django 2.1.7 on 2019-11-14 17:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0006_auto_20191113_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='approved_participants',
            field=models.ManyToManyField(blank=True, related_name='aproved', to=settings.AUTH_USER_MODEL),
        ),
    ]
