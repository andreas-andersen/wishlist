# Generated by Django 3.2.5 on 2021-07-26 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210718_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='has_submitted',
        ),
    ]