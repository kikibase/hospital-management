# Generated by Django 4.0.3 on 2022-04-23 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0020_alter_doctor_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='nurse',
            name='Profile_image',
            field=models.ImageField(blank=True, default='Null', null=True, upload_to=''),
        ),
    ]
