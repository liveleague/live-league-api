# Generated by Django 2.2.2 on 2019-07-11 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_artist_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promoter',
            name='points',
        ),
    ]