# Generated by Django 5.0.1 on 2024-02-26 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userData', '0005_alter_userdata_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile',
            name='pdf_file',
            field=models.FileField(upload_to='user/pdf_files/'),
        ),
        migrations.AlterField(
            model_name='userfile',
            name='user_file',
            field=models.FileField(upload_to='user/user_files/'),
        ),
    ]
