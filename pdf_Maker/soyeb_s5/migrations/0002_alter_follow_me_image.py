# Generated by Django 4.2.3 on 2024-01-08 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soyeb_s5', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow_me',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='admin_content/'),
        ),
    ]
