# Generated by Django 5.0.6 on 2024-05-29 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0003_user_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_on', models.DateTimeField(auto_created=True)),
                ('instructor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='base.instructor')),
                ('learner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='base.learner')),
            ],
        ),
    ]
