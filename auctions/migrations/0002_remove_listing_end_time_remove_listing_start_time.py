# Generated by Django 5.0.1 on 2024-04-25 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='start_time',
        ),
    ]
