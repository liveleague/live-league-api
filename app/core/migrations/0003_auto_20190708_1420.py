# Generated by Django 2.2.2 on 2019-07-08 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_event_tickets_remaining'),
    ]

    operations = [
        migrations.AddField(
            model_name='tally',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tally',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineup', to='core.Event'),
        ),
    ]
