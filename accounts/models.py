import hashlib
from django.apps import apps
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.fields import EmailField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_leader', True)
        kwargs.setdefault('is_self_responsible', True)
        kwargs.setdefault('first_name', 'Admin')
        kwargs.setdefault('last_name', 'Adminson')

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if kwargs.get('is_leader') is not True:
            raise ValueError('Superuser must have is_leader=True.')
        return self.create_user(email, password, **kwargs)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        'email address',
        blank=False,
        null=False,
        unique=True
    )
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()

    first_name = models.CharField(
        max_length=30, 
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=30, 
        null=True,
        blank=True,
    )
    is_leader = models.BooleanField(
        default=False,
    )
    assigned_to = models.ForeignKey(
        'CustomUser', 
        null=True, 
        blank=True,
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    responsible_by = models.ForeignKey(
        'CustomUser',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='responsibilities',
    )
    is_self_responsible = models.BooleanField(
        default=True
    )
    def get_gravatar(self):
        md5 = hashlib.md5(self.email.encode())
        digest = md5.hexdigest()
        SIZE = 40
        DEFAULT = 'identicon'

        return f'http://www.gravatar.com/avatar/{digest}?s={SIZE}&d={DEFAULT}'

    def get_email_30char(self):
        if len(self.email) > 30:
            output = self.email[:29] + '...'
        else: 
            output = self.email
        return output

    def get_notifications(self):
        notifications = Notification.objects.filter(user=self).filter(read=False)
        return len(notifications)

    def check_multi_responsible(self):
        responsibilities = CustomUser.objects.filter(responsible_by=self.pk)

        return len(responsibilities) > 1

    def __str__(self):
        if self.first_name == None and self.last_name == None:
            return ' '
        else:
            return self.first_name + ' ' + self.last_name


class Notification(models.Model):
    user = models.ForeignKey(
        'CustomUser',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='user'
    )
    INVITATION = 'INV'
    OTHER = 'ETC'
    type_choices = [
        (INVITATION, 'Invitation'),
        (OTHER, 'Other'),
    ]
    type = models.CharField(
        max_length=3,
        choices=type_choices,
        default=OTHER,
        blank=False
    )
    group = models.ForeignKey(
        'groups.CustomGroup',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='group'
    )
    context_user = models.ForeignKey(
        'CustomUser',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='context_user'
    )
    content = models.TextField(
        blank=True
    )
    read = models.BooleanField(
        null=False,
        blank=False,
        default=False,
    )
    created = models.DateTimeField(auto_now_add=True)