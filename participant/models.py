from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
from django.core.validators import MinValueValidator
import uuid


# Define user manager
class UserManager(BaseUserManager):
    def create_user(self, multipass_username, name, email, CWID, authorized_requester=False, reward_balance=0,
                    password=None):
        if not multipass_username:
            raise ValueError("Enter your Mines username")
        user = self.model(
            multipass_username=multipass_username,
            name=name,
            email=email,
            CWID=CWID,
            authorized_requester=authorized_requester,
            reward_balance=reward_balance,
        )
        # To be removed
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, multipass_username, name, email, CWID, authorized_requester, reward_balance,
                         password=None):
        user = self.create_user(multipass_username, name, email, CWID, authorized_requester, reward_balance, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    multipass_username = models.CharField(max_length=50, unique=True, )
    name = models.CharField(max_length=100, )
    email = models.EmailField()
    CWID = models.IntegerField(primary_key=True, )
    authorized_requester = models.BooleanField(default=False, )
    reward_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, )
    is_superuser = models.BooleanField(default=False, )
    is_staff = models.BooleanField(default=False, )
    # completed_tasks = ManyToMany(Task) maybe?

    objects = UserManager()

    REQUIRED_FIELDS = ['name', 'email', 'CWID', 'authorized_requester', 'reward_balance']

    USERNAME_FIELD = 'multipass_username'
    # def set_unusable_password(self):
    # Set a value that will never be a valid hash
    # self.password = make_password(None)

    def __str__(self):
        return self.name


class Task(models.Model):
    PENDING = 'PE'
    ACTIVE = 'AC'
    COMPLETED = 'CO'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
    ]

    link_to = models.URLField(max_length=200, blank=False)
    participant_qualifications = models.CharField(max_length=100, blank=True)
    reward_amount = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=0.00)
    max_num_participants = models.PositiveIntegerField(default=0, blank=True, validators=[MinValueValidator(1)])
    title = models.CharField(max_length=100, blank=False)
    payment_index = models.IntegerField(blank=False)
    description = models.TextField(max_length=1024, blank=False)
    posted_date = models.DateField(auto_now_add=True, blank=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    end_date = models.DateField(blank=False)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='req')
    participants = models.ManyToManyField(User, blank=True, related_name='part')
    approved_participants = models.ManyToManyField(User, blank=True, related_name='aproved')

    def __str__(self):
        return self.title


class Tag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, blank=False)

    @classmethod
    def create(cls, tag, task):
        new_tag = cls(tag=tag, task=task)
        return new_tag

    def __str__(self):
        return self.tag


class Transaction(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, )
    amount = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=0.00, )
    processed = models.BooleanField(default=False, )

    @classmethod
    def create(cls, recipient, amount):
        transaction = cls(recipient = recipient, amount = amount, processed = False)
        return transaction

    def __str__(self):
        return str(self.amount) + " to " + self.recipient.name
