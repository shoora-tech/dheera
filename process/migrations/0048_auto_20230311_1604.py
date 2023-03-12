# Generated by Django 3.2.18 on 2023-03-11 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0047_auto_20230311_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentterms',
            name='advacne_tt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_term', to='process.advancett'),
        ),
        migrations.AlterField(
            model_name='paymentterms',
            name='balance_term',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_term', to='process.balanceterm'),
        ),
        migrations.AlterField(
            model_name='paymentterms',
            name='days_eta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_term', to='process.dayseta'),
        ),
    ]
