# Generated by Django 3.2.18 on 2023-03-08 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0016_poremarks_purchaseorder_purchaseordersku'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='pi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='process.performainvoice'),
        ),
    ]