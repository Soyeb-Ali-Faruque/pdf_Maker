# Generated by Django 4.2.3 on 2023-12-03 12:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userData', '0003_userfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfile',
            name='date',
        ),
        migrations.RemoveField(
            model_name='userfile',
            name='time',
        ),
        migrations.AddField(
            model_name='userfile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
