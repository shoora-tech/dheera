# Generated by Django 3.2.18 on 2023-03-11 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0050_location_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='performainvoice',
            name='destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='destination_performa_invoice', to='process.location', verbose_name='Destination'),
        ),
        migrations.AlterField(
            model_name='performainvoice',
            name='from_port',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_performa_invoice', to='process.location', verbose_name='Port of Loading'),
        ),
        migrations.AlterField(
            model_name='performainvoice',
            name='to_port',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_performa_invoice', to='process.location', verbose_name='Port of Discharge'),
        ),
    ]