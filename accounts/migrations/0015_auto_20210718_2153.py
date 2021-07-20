# Generated by Django 3.2.5 on 2021-07-18 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_customuser_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='has_submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_leader',
            field=models.BooleanField(default=False),
        ),
    ]