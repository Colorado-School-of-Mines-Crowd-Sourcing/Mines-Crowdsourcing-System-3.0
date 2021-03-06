# Generated by Django 2.1.7 on 2019-11-12 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0004_merge_20191106_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participantcompletedtask',
            name='task',
        ),
        migrations.RemoveField(
            model_name='participantcompletedtask',
            name='user',
        ),
        migrations.RemoveField(
            model_name='requesteractivetask',
            name='task',
        ),
        migrations.RemoveField(
            model_name='requesteractivetask',
            name='user',
        ),
        migrations.RemoveField(
            model_name='requesterpasttask',
            name='task',
        ),
        migrations.RemoveField(
            model_name='requesterpasttask',
            name='user',
        ),
        migrations.AddField(
            model_name='task',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='participants',
            field=models.ManyToManyField(related_name='part', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='req', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ParticipantCompletedTask',
        ),
        migrations.DeleteModel(
            name='RequesterActiveTask',
        ),
        migrations.DeleteModel(
            name='RequesterPastTask',
        ),
    ]
