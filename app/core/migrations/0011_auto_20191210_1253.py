# Generated by Django 3.0 on 2019-12-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_user_stripe_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='stripe_id',
            new_name='stripe_customer_id',
        ),
        migrations.AddField(
            model_name='user',
            name='stripe_account_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
