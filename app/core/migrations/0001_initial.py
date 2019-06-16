# Generated by Django 2.2.2 on 2019-06-14 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('facebook', models.URLField(blank=True)),
                ('instagram', models.URLField(blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('soundcloud', models.URLField(blank=True)),
                ('spotify', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('website', models.URLField(blank=True)),
                ('youtube', models.URLField(blank=True)),
                ('is_artist', models.BooleanField(default=False)),
                ('is_promoter', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('points', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('core.user', models.Model),
        ),
        migrations.CreateModel(
            name='Promoter',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('is_verified', models.BooleanField(default=False)),
                ('points', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('core.user', models.Model),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1000)),
                ('end_time', models.DateTimeField()),
                ('name', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='core.Venue')),
                ('artists', models.ManyToManyField(related_name='events', to='core.Artist')),
                ('promoter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='core.Promoter')),
            ],
        ),
    ]
