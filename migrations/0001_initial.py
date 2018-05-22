# Generated by Django 2.0.4 on 2018-04-12 10:57

import uuid

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TerraUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='unique identifier')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('properties', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='FeatureRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('properties', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='relations_as_destination', to='terra.Feature')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='relations_as_origin', to='terra.Feature')),
            ],
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('schema', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='LayerRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='relations_as_destination', to='terra.Layer')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='relations_as_origin', to='terra.Layer')),
            ],
        ),
        migrations.AddField(
            model_name='feature',
            name='layer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='terra.Layer'),
        ),
    ]
