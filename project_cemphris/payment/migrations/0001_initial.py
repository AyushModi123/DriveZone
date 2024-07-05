# Generated by Django 4.2.13 on 2024-07-05 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('base', '0007_alter_licenseinformation_issuing_authority_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('failed', 'Failed'), ('complete', 'Complete')], default='pending')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='course.course')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='base.learner')),
            ],
        ),
    ]
