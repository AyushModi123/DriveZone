# Generated by Django 5.0.6 on 2024-06-24 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_instructor_full_name_alter_instructor_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='full_name',
            field=models.CharField(max_length=255),
        ),
    ]