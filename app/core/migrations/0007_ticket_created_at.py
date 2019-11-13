# Generated by Django 2.2.5 on 2019-11-05 10:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_user_is_temporary'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
