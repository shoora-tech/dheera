# Generated by Django 3.2.18 on 2023-03-07 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tyre', '0007_auto_20230307_1318'),
        ('supplier', '0003_suppliersku_is_past'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliersku',
            name='is_past',
        ),
        migrations.AddField(
            model_name='supplierskusummary',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_sku_summary', to='tyre.brand'),
        ),
        migrations.AddField(
            model_name='supplierskusummary',
            name='cost',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='supplierskusummary',
            name='number_of_containers',
            field=models.FloatField(null=True, verbose_name='No. of containers'),
        ),
        migrations.AddField(
            model_name='supplierskusummary',
            name='pattern',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_sku_summary', to='tyre.pattern'),
        ),
        migrations.AddField(
            model_name='supplierskusummary',
            name='pr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_sku_summary', to='tyre.pr'),
        ),
        migrations.AddField(
            model_name='supplierskusummary',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='supplierskusummary',
            name='stuff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_sku_summary', to='tyre.stuff'),
        ),
        migrations.AddField(
            model_name='supplierskusummary',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_sku_summary', to='supplier.supplier'),
        ),
        migrations.AddField(
            model_name='supplierskusummary',
            name='tyre_set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_sku_summary', to='tyre.tyreset'),
        ),
        migrations.AddField(
            model_name='supplierskusummary',
            name='tyre_size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_sku_summary', to='tyre.tyresize'),
        ),
        migrations.AlterField(
            model_name='supplierskusummary',
            name='sku',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_sku_summary', to='supplier.suppliersku'),
        ),
    ]
