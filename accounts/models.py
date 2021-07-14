import hashlib
import urllib
from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class CustomUser(AbstractUser):
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

    def get_gravatar(self):
        md5 = hashlib.md5(self.email.encode())
        digest = md5.hexdigest()
        SIZE = 40

        return f'http://www.gravatar.com/avatar/{digest}?s={SIZE}'