# Generated by Django 5.0.6 on 2024-06-07 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_organisation_instructor_organisation'),
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='organisation',
        ),
        migrations.AddField(
            model_name='instructor',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instructors', to='school.school'),
        ),
        migrations.DeleteModel(
            name='Organisation',
        ),
    ]
