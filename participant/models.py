from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField
import uuid
import random


# Define user manager
class UserManager(BaseUserManager):
    def create_user(self, name, email, CWID, authorized_requester=False, reward_balance=0,
                    password=None):
        if not name:
            raise ValueError("Enter your a username")
        user = self.model(
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

    def create_superuser(self, name, email, CWID, authorized_requester, reward_balance,
                         password=None):
        user = self.create_user(name, email, CWID, authorized_requester, reward_balance, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

SEX_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)
ETHNICITY_CHOICES = (
    ('White', 'White'),
    ('Hispanic or Latino', 'Hispanic or Latino'),
    ('Black or African American', 'Black or African American'),
    ('Native American or American Indian', 'Native American or American Indian'),
    ('Asian/Pacific Islander', 'Asian/Pacific Islander'),
    ('Other', 'Other'),
)
MAJOR_CHOICES = (
    ('Applied Mathematics and Statistics', 'Applied Mathematics and Statistics'),
    ('Biochemistry', 'Biochemistry'),
    ('Chemical Engineering', 'Chemical Engineering'),
    ('Chemistry', 'Chemistry'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Computer Science', 'Computer Science'),
    ('Economics', 'Economics'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Engineering', 'Engineering'),
    ('Engineering Physics', 'Engineering Physics'),
    ('Environmental Engineering', 'Environmental Engineering'),
    ('Geological Engineering', 'Geological Engineering'),
    ('Geophysical Engineering', 'Geophysical Engineering'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Metallurgical and Materials Engineering', 'Metallurgical and Materials Engineering'),
    ('Mining Engineering', 'Mining Engineering'),
    ('Petroleum Engineering', 'Petroleum Engineering'),
    ('Not a Mines Student', 'Not a Mines Student'),
)

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    CWID = models.IntegerField(primary_key=True, )
    authorized_requester = models.BooleanField(default=False, )
    reward_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, )
    is_superuser = models.BooleanField(default=False, )
    is_staff = models.BooleanField(default=False, )
    anon_id = models.IntegerField(blank=True, unique=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default='Female')
    ethnicity = models.CharField(max_length=100, choices=ETHNICITY_CHOICES, default='Other')
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)], default=18)
    major = models.CharField(max_length=100, choices=MAJOR_CHOICES, default='Not a Mines Student')
    # completed_tasks = ManyToMany(Task) maybe?

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'CWID', 'authorized_requester', 'reward_balance']

    USERNAME_FIELD = 'name'
    def save(self, *args, **kwargs):
        if not self.anon_id:
            is_unique = False
            while not is_unique:
                random_number = random.randint(100000,999999)
                print(random_number)
                same_anon_id = User.objects.filter(anon_id=random_number)
                if (same_anon_id.count() == 0):
                    is_unique = True
            self.anon_id = random_number
        super(User, self).save(*args, **kwargs)

    # def set_unusable_password(self):
    # Set a value that will never be a valid hash
    # self.password = make_password(None)
    def __str__(self):
        #return self.name
        return self.anon_id


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
    paid_participants = models.ManyToManyField(User, blank=True, related_name='paid')
    major_qualifications = MultiSelectField(choices=MAJOR_CHOICES, blank=False, default='Applied Mathematics and Statistics,Biochemistry,Chemical Engineering,Chemistry,Civil Engineering,Computer Science,Economics,Electrical Engineering,Engineering,Engineering Physics,Environmental Engineering,Geological Engineering,Geophysical Engineering,Mechanical Engineering,Metallurgical and Materials Engineering,Mining Engineering,Petroleum Engineering,Not a Mines Student')
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
