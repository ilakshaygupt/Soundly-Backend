# Generated by Django 4.2.6 on 2023-10-28 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_activetoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_valid',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='ActiveToken',
        ),
    ]
