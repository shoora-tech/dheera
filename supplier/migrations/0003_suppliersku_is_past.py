# Generated by Django 3.2.18 on 2023-03-07 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_suppliersku_supplierskusummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliersku',
            name='is_past',
            field=models.BooleanField(default=False),
        ),
    ]
