import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


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
        kwargs.setdefault('is_leader', True)

        if kwargs.get('is_leader') is not True:
            raise ValueError('Superuser must have is_leader=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
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
        default=True,
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

    def save(self, *args, **kwargs):
        self.is_self_responsible = self.responsible_by.email == self.email
        super(CustomUser, self).save(*args, **kwargs)

    def get_gravatar(self):
        md5 = hashlib.md5(self.email.encode())
        digest = md5.hexdigest()
        SIZE = 30

        return f'http://www.gravatar.com/avatar/{digest}?s={SIZE}'

    def check_multi_responsible(self):
        responsibilities = CustomUser.objects.filter(responsible_by=self.pk)

        return len(responsibilities) > 1

    def __str__(self):
        return self.email