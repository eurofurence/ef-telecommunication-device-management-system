# Generated by Django 5.0.4 on 2024-05-03 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='radioaccessorytemplate',
            name='compatible_with',
            field=models.ManyToManyField(blank=True, help_text='Item templates this accessory is compatible with', related_name='+', to='backend.itemtemplate'),
        ),
    ]
