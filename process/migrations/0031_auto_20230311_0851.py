# Generated by Django 3.2.18 on 2023-03-11 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0030_costsheet_total_vip_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='costsheetsku',
            name='purchase_price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='costsheetsku',
            name='sales_price',
            field=models.FloatField(null=True),
        ),
    ]
