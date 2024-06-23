# Generated by Django 5.0.6 on 2024-06-23 16:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='description',
        ),
        migrations.AddField(
            model_name='school',
            name='image_url',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='school',
            name='location',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='mobile_number',
            field=models.CharField(default='0000000000', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='preferred_language',
            field=models.CharField(default='English', null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='school',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='school', to=settings.AUTH_USER_MODEL),
        ),
    ]
