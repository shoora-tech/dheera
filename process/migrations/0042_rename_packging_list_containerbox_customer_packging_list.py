# Generated by Django 3.2.18 on 2023-03-11 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0041_auto_20230311_1447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='containerbox',
            old_name='packging_list',
            new_name='customer_packging_list',
        ),
    ]
