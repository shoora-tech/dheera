# Generated by Django 3.2.18 on 2023-03-10 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0025_auto_20230310_1616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='costsheetsku',
            old_name='dcp',
            new_name='discount_amount',
        ),
        migrations.RenameField(
            model_name='costsheetsku',
            old_name='discount',
            new_name='discount_percentage',
        ),
    ]
