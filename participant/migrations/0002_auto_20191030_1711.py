# Generated by Django 2.1.7 on 2019-10-30 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participantcompletedtask',
            options={'verbose_name': 'Completed task', 'verbose_name_plural': 'Completed tasks'},
        ),
        migrations.RenameField(
            model_name='task',
            old_name='min_participant_req',
            new_name='max_num_participants',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='ideal_participant',
            new_name='participant_qualifications',
        ),
    ]
