# Generated by Django 4.2.18 on 2025-02-03 02:21

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=cloudinary.models.CloudinaryField(blank=True, default='default_profile_lhtmj4', max_length=255, null=True, verbose_name='image'),
        ),
    ]
