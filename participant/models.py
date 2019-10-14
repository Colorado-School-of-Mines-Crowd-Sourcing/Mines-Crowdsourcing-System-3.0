from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
import uuid


#Define user manager
class UserManager(BaseUserManager):
    def create_user(self, multipass_username, name, email, CWID, authorized_requester=False, reward_balance=0, password=None):
        if not multipass_username:
            raise ValueError("Enter your Mines username")
        user = self.model(
            multipass_username = multipass_username,
            name = name,
            email = email,
            CWID = CWID,
            authorized_requester = authorized_requester,
            reward_balance = reward_balance,
        )
        user.save()
        return user

    def create_superuser(self, multipass_username, name, email, CWID, authorized_requester, reward_balance, password=None):
        user = self.create_user(multipass_username, name, email, CWID, authorized_requester, reward_balance)
        user.is_superuser = True
        user.save()
        return user

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    user_ID = models.AutoField(primary_key=True,)
    multipass_username = models.CharField(max_length=50, unique=True, )
    name = models.CharField(max_length=100, )
    email = models.EmailField()
    CWID = models.IntegerField(unique=True, )
    authorized_requester = models.BooleanField(default=False, )
    reward_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, )
    is_superuser = models.BooleanField(default=False, )

    objects = UserManager()

    REQUIRED_FIELDS=['name', 'email', 'CWID', 'authorized_requester', 'reward_balance']

    USERNAME_FIELD = 'multipass_username'
    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)


class ParticipantCompletedTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_ID = models.IntegerField(blank=False)


class RequesterActiveTaskID(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_ID = models.IntegerField(blank=False)


class RequesterPastTaskId(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_ID = models.IntegerField(blank=False)


class Task(models.Model):
    task_ID = models.AutoField(primary_key=True, blank=False)
    link_to = models.URLField(max_length=50, blank=False)
    ideal_participant = models.CharField(max_length=100, blank=False)
    reward_amount = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=0.00, min_value=0.0)
    min_participant_req = models.IntegerField(default=0, blank=True, min_value=0)
    title = models.CharField(max_length=100, blank=False)
    payment_index = models.IntegerField(blank=False)
    description = models.TextField(max_length=1024, blank=False)
    posted_date = models.DateField(auto_now_add=True, blank=False)
    end_date = models.DateField(blank=False)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, blank=False)
