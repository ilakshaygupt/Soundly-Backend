# Generated by Django 4.2.6 on 2023-11-09 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_myuser_profile_pic_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='is_artist',
            new_name='is_uploader',
        ),
    ]