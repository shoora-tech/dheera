# Generated by Django 3.2.18 on 2023-03-08 12:35

from django.db import migrations, models
import django.db.models.deletion
import process.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0004_auto_20230307_1556'),
        ('tyre', '0007_auto_20230307_1318'),
        ('customer', '0001_initial'),
        ('process', '0015_auto_20230308_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='PORemarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('remarks', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('po_number', models.CharField(blank=True, default=process.models.get_po_number, max_length=60, null=True)),
                ('po_date', models.DateField(null=True)),
                ('country_of_origin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order', to='customer.country')),
                ('from_port', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_purchase_order', to='process.location')),
                ('packing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order', to='process.packingtype')),
                ('payment_terms', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order', to='process.paymentterms')),
                ('po_remarks', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order', to='process.poremarks')),
                ('sender_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order', to='process.senderaddress')),
                ('shipping_marks', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order', to='process.shippingmarks')),
                ('supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order', to='supplier.supplier')),
                ('to_port', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_purchase_order', to='process.location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=0)),
                ('number_of_containers', models.FloatField(blank=True, null=True, verbose_name='No. of containers')),
                ('expected_price', models.FloatField(blank=True, null=True)),
                ('expected_total_cost', models.FloatField(blank=True, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='po_sku', to='tyre.brand')),
                ('pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='po_sku', to='tyre.pattern')),
                ('po', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='po_sku', to='process.purchaseorder')),
                ('pr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='po_sku', to='tyre.pr')),
                ('stuff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='po_sku', to='tyre.stuff')),
                ('tyre_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='po_sku', to='tyre.tyreset')),
                ('tyre_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='po_sku', to='tyre.tyresize')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
