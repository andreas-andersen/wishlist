import hashlib, locale
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

    def check_multi_responsible(self):
        responsibilities = CustomUser.objects.filter(responsible_by=self.pk)

        return len(responsibilities) > 1

    def __str__(self):
        return self.username


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

    def __str__(self):
        return self.name

class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(microsecond=0)
            return val.isoformat()
        return ''