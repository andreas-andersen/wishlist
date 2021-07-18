from django.db import models
from accounts.models import CustomUser
from django.contrib.auth.models import Group

class CustomGroup(Group):
    leader = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='leader'
    )
    max_gift_value = models.DecimalField(
        max_digits=20,
        decimal_places=2, 
        null=True,
        blank=True,
    )
    DKK = 'DKK'
    NOK = 'NOK'
    JPY = '¥'
    USD = "$"
    currency_choices = [
        (DKK, 'DKK'),
        (NOK, 'NOK'),
        (JPY, '¥'),
        (USD, '$'),
    ]
    currency = models.CharField(
        max_length=3,
        choices=currency_choices,
        default=NOK,
    )
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name
