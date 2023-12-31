# Generated by Django 4.2.6 on 2023-11-25 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("music", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="song",
            name="lyrics_json",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="favourite",
            name="artist",
            field=models.ManyToManyField(to="music.artist"),
        ),
        migrations.AlterField(
            model_name="favourite",
            name="language",
            field=models.ManyToManyField(to="music.language"),
        ),
        migrations.AlterField(
            model_name="favourite",
            name="playlist",
            field=models.ManyToManyField(to="music.playlist"),
        ),
        migrations.AlterField(
            model_name="favourite",
            name="song",
            field=models.ManyToManyField(to="music.song"),
        ),
        migrations.AlterField(
            model_name="favourite",
            name="user",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="playlist",
            name="songs",
            field=models.ManyToManyField(blank=True, default=None, to="music.song"),
        ),
    ]
