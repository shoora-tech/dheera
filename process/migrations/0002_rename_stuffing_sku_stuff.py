# Generated by Django 3.2.18 on 2023-03-07 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sku',
            old_name='stuffing',
            new_name='stuff',
        ),
    ]
