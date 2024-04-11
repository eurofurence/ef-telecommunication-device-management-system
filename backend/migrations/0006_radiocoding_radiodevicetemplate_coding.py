# Generated by Django 4.2.11 on 2024-04-11 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadioCoding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the coding', max_length=64)),
                ('color', models.CharField(help_text='Color of the coding in hex format', max_length=7)),
                ('description', models.TextField(blank=True, help_text='Description of the coding', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='radiodevicetemplate',
            name='coding',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.PROTECT, to='backend.radiocoding'),
            preserve_default=False,
        ),
    ]
