# Generated by Django 4.2.13 on 2024-07-05 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_licenseinformation_issuing_authority_and_more'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnerCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled', to='course.course')),
                ('learner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='base.learner')),
            ],
        ),
    ]
