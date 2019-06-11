# Generated by Django 2.2.2 on 2019-06-11 09:41

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_promoter_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
    ]
