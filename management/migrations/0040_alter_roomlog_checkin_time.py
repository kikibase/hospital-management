# Generated by Django 4.0.1 on 2022-07-19 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0039_room_avaialble_beds_alter_roomlog_bed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomlog',
            name='checkin_time',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
