# Generated by Django 4.2.13 on 2024-07-12 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_paymentdetails_paymentdetail'),
        ('course', '0003_enrollcourse_delete_learnercourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollcourse',
            name='payment',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='enroll', to='payment.paymentdetail'),
            preserve_default=False,
        ),
    ]
