# Generated by Django 4.2.6 on 2023-11-05 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favourite',
            name='language',
        ),
        migrations.RemoveField(
            model_name='favourite',
            name='playlist',
        ),
        migrations.RemoveField(
            model_name='favourite',
            name='song',
        ),
        migrations.AddField(
            model_name='favourite',
            name='language',
            field=models.ManyToManyField(blank=True, null=True, to='music.language'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='playlist',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='music.playlist'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='song',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='music.song'),
        ),
    ]
