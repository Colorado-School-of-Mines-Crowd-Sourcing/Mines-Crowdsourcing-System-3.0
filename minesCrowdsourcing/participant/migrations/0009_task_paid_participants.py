# Generated by Django 3.1.1 on 2020-11-07 23:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0008_auto_20191121_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='paid_participants',
            field=models.ManyToManyField(blank=True, related_name='paid', to=settings.AUTH_USER_MODEL),
        ),
    ]
