# Generated by Django 4.0.1 on 2022-07-14 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0026_rename_staff_phone_number_staff_type_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='Appointment_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
