# Generated by Django 3.2.5 on 2021-07-16 09:30

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('max_gift_value', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('currency', models.CharField(choices=[('DKK', 'DKK'), ('NOK', 'NOK'), ('¥', '¥'), ('$', '$')], default='NOK', max_length=3)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leader', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
    ]
