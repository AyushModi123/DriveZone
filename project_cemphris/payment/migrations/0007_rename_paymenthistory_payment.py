# Generated by Django 5.0.6 on 2024-06-01 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_instructor_user_alter_learner_user'),
        ('booking', '0005_alter_book_booked_on'),
        ('payment', '0006_rename_payment_paymenthistory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PaymentHistory',
            new_name='Payment',
        ),
    ]
