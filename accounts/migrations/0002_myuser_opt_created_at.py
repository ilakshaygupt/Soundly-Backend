# Generated by Django 4.2.6 on 2023-11-23 05:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="myuser",
            name="opt_created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
