# Generated by Django 4.2.6 on 2023-11-13 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0012_alter_song_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='thumbnail_url',
            field=models.URLField(blank=True, default='https://community.spotify.com/t5/image/serverpage/image-id/25294i2836BD1C1A31BDF2?v=v2', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
