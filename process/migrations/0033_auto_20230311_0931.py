# Generated by Django 3.2.18 on 2023-03-11 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0032_auto_20230311_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costsheet',
            name='freight_purchase',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='costsheet',
            name='freight_sale',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='costsheet',
            name='insurance_purchase',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='costsheet',
            name='insurance_sale',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='costsheet',
            name='total_advt_percentage',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='costsheet',
            name='total_discount_percentage',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='costsheet',
            name='total_vip_percentage',
            field=models.FloatField(default=0, null=True),
        ),
    ]