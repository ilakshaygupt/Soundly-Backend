# Generated by Django 4.2.6 on 2023-10-23 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_myuser_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='otp',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
