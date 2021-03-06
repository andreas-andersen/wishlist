from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from groups.models import CustomGroup

class Wish(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        CustomGroup,
        on_delete=models.CASCADE
    )
    HIGH_PRIORITY = 'HI'
    MEDIUM_PRIORITY = 'MD'
    LOW_PRIORITY = 'LO'
    priority_choices = [
        (HIGH_PRIORITY, 'High'),
        (MEDIUM_PRIORITY, 'Medium'),
        (LOW_PRIORITY, 'Low'),
    ]
    priority = models.CharField(
        max_length=2,
        choices=priority_choices,
        default=HIGH_PRIORITY,
        blank=True
    )
    details = models.TextField(blank=True)
    link = models.URLField(
        max_length=500,
        blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wish_detail', args=[str(self.id)])

    class Meta:
        verbose_name_plural = 'Wishes'