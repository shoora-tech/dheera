# Generated by Django 3.2.18 on 2023-03-11 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0028_auto_20230311_0840'),
    ]

    operations = [
        migrations.RenameField(
            model_name='costsheet',
            old_name='freight_purchae',
            new_name='freight_purchase',
        ),
        migrations.AddField(
            model_name='costsheet',
            name='freight_sale',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='costsheet',
            name='insurance_sale',
            field=models.FloatField(null=True),
        ),
    ]