# Generated by Django 4.2.3 on 2023-12-03 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userData', '0002_userdata_name_userdata_profile_picture_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_file', models.FileField(upload_to='user_files/')),
                ('pdf_file', models.FileField(upload_to='pdf_files/')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userData.userdata')),
            ],
        ),
    ]
