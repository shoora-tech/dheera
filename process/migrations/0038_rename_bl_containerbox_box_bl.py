# Generated by Django 3.2.18 on 2023-03-11 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0037_auto_20230311_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='containerbox',
            old_name='bl',
            new_name='box_bl',
        ),
    ]
