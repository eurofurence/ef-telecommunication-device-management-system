# Generated by Django 5.0.4 on 2024-04-24 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_callbox_camera_dhcp_callbox_camera_network'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCoordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.IntegerField(help_text='Floor number of the item location')),
                ('latitude', models.FloatField(help_text='Latitude of the item location')),
                ('longitude', models.FloatField(help_text='Longitude of the item location')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='coordinates',
            field=models.OneToOneField(blank=True, default=None, help_text='Coordinates of the item on the deployment map', null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.itemcoordinates'),
        ),
    ]
