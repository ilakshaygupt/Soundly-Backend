# Generated by Django 4.2.6 on 2023-11-10 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_artist_song_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='description',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='thumbnail_url',
            field=models.URLField(blank=True, default='https://community.spotify.com/t5/image/serverpage/image-id/25294i2836BD1C1A31BDF2?v=v2', null=True),
        ),
    ]
