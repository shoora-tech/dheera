# Generated by Django 3.2.18 on 2023-03-11 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0048_auto_20230311_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='price_term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotation', to='process.priceterms'),
        ),
    ]
