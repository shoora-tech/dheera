# Generated by Django 3.2.18 on 2023-03-07 13:25

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0005_auto_20230307_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sku',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='sku',
            name='exchange_rate',
        ),
        migrations.AddField(
            model_name='quotation',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.expressions.Case, related_name='quotation', to='process.currency'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='exchange_rate',
            field=models.FloatField(null=True),
        ),
    ]