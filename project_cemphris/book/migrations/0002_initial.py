# Generated by Django 5.0.6 on 2024-05-29 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='payment.payment'),
        ),
    ]
