from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
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