# Generated by Django 2.1.7 on 2019-10-17 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='ideal_participant',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
