from django.db import models
from django.db.models.fields.related import ForeignKey
from accounts.models import CustomUser
from django.contrib.auth.models import Group

class CustomGroup(Group):
    invited_users = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='invited_users',
    )
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

class Assignment(models.Model):
    member = ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='member',
    )
    assignment = ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='assignment',
    )

    def __str__(self):
        return self.member.email + '|' + self.assignment.email

    class Meta:
        verbose_name_plural = 'Assignment'

class Assignments(models.Model):
    group = models.ForeignKey(
        'CustomGroup',
        blank=True,
        on_delete=models.CASCADE
    )
    assignments = models.ManyToManyField('Assignment')
    time = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.group.name + ' assignments'

    class Meta:
        verbose_name_plural = 'Assignments'