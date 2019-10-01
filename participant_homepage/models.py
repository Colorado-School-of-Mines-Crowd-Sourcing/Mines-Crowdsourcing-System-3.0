from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
import uuid


# Create your models here.
class Users(AbstractBaseUser):
    user_ID = models.AutoField(primary_key=True, blank=False)
    multipass_username = models.CharField(max_length=50, unique=True, blank=False)
    name = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=50, blank=False)
    CWID = models.IntegerField(unique=True, blank=False)
    authorized_requester = models.BooleanField(blank=False, default=False)
    reward_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class ParticipantCompletedTasks(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    task_ID = models.IntegerField(blank=False)


class RequesterActiveTaskID(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    task_ID = models.IntegerField(blank=False)


class RequesterPastTaskId(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    task_ID = models.IntegerField(blank=False)


class Task(models.Model):
    task_ID = models.AutoField(primary_key=True, blank=False)
    link_to = models.CharField(max_length=50, blank=False)
    reward_amount = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=0.00)
    min_participant_req = models.IntegerField
    title = models.CharField(max_length=100, blank=False)
    payment_index = models.IntegerField(blank=False)
    description = models.CharField(max_length=1024, blank=False)
    posted_date = models.DateField(auto_now_add=True, blank=False)
    end_date = models.DateField(blank=False)


class Tags(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, blank=False)
