# Generated by Django 4.0.3 on 2022-04-08 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_room_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='Room_availability',
            field=models.BooleanField(default=True),
        ),
    ]
