# Generated by Django 4.2.6 on 2023-11-07 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='profile_pic_url',
            field=models.URLField(default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlfrScK05sZxTgh7Bg4p_Anm_ZSxxqGHpCFA&usqp=CAU'),
        ),
    ]