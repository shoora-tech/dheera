# Generated by Django 3.2.18 on 2023-03-11 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0040_auto_20230311_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='containerbox',
            name='measurement',
            field=models.FloatField(default=0, verbose_name='Measurement (CBM)'),
        ),
        migrations.AddField(
            model_name='containerbox',
            name='packging_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='container_box', to='process.packaginglist'),
        ),
        migrations.AddField(
            model_name='containerbox',
            name='total_container_weight',
            field=models.FloatField(default=0, verbose_name='Total Weight (KGS)'),
        ),
    ]
