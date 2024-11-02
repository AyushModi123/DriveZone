# Generated by Django 4.2.13 on 2024-07-12 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_licenseinformation_issuing_authority_and_more'),
        ('payment', '0002_rename_paymentdetails_paymentdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentdetail',
            name='course',
        ),
        migrations.AddField(
            model_name='paymentdetail',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='base.school'),
            preserve_default=False,
        ),
    ]
