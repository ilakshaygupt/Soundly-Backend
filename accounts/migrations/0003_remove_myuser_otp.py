# Generated by Django 4.2.6 on 2023-10-23 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_myuser_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='otp',
        ),
    ]
