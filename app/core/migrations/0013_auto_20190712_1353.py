# Generated by Django 2.2.3 on 2019-07-12 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20190711_1738'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tickettype',
            old_name='capacity',
            new_name='tickets_remaining',
        ),
    ]