# Generated by Django 5.0.6 on 2024-06-02 10:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_instructor_area_of_expertise_instructor_experience_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(default=datetime.datetime(2024, 6, 2, 10, 33, 7, 34766, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
