# Generated by Django 4.2.6 on 2023-11-25 15:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("music", "0004_alter_song_lyrics_json"),
    ]

    operations = [
        migrations.AlterField(
            model_name="song",
            name="lyrics_json",
            field=models.JSONField(blank=True, default="[]", null=True),
        ),
    ]
