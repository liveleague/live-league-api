# Generated by Django 2.2.2 on 2019-06-11 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190611_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='description',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='promoter',
            name='description',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
