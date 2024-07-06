# Generated by Django 4.2.13 on 2024-07-06 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_licenseinformation_issuing_authority_and_more'),
        ('course', '0002_learnercourse'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnrollCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learner_courses', to='course.course')),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='learner_courses', to='base.instructor')),
                ('learner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='learner_course', to='base.learner')),
            ],
        ),
        migrations.DeleteModel(
            name='LearnerCourse',
        ),
    ]
