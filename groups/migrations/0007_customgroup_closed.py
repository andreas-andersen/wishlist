# Generated by Django 3.2.5 on 2021-07-28 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_auto_20210728_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='customgroup',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
