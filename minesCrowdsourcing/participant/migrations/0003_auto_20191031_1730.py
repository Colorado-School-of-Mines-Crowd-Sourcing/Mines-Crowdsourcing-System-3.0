# Generated by Django 2.2.4 on 2019-10-31 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0002_auto_20191024_2124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='max_participant',
            new_name='max_num_participants',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='ideal_participant',
            new_name='participant_qualifications',
        ),
    ]
