# Generated by Django 5.0.6 on 2024-06-25 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_instructor_area_of_expertise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='area_of_expertise',
            field=models.CharField(choices=[('motorbike', 'Motorbike'), ('car', 'Car'), ('truck', 'Truck')]),
        ),
    ]
