# Generated by Django 2.2.2 on 2019-06-16 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190616_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='artists',
            field=models.ManyToManyField(related_name='events', to='core.Artist'),
        ),
    ]
