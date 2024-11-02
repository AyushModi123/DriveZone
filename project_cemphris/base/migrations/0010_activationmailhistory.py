# Generated by Django 4.2.13 on 2024-07-18 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_school_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationMailHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('sent_count', models.SmallIntegerField(default=0)),
            ],
        ),
    ]
