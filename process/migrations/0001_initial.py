# Generated by Django 3.2.18 on 2023-03-07 12:36

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('tyre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvanceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_value', models.FloatField(blank=True, null=True)),
                ('total_quantity', models.FloatField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation', to='customer.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('exchange_rate', models.FloatField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku', to='tyre.brand')),
                ('currency', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='sku', to='process.currency')),
                ('pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku', to='tyre.pattern')),
                ('payment_basis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku', to='tyre.paymentbasis')),
                ('pr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku', to='tyre.pr')),
                ('quotaion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku', to='process.quotation')),
                ('stuffing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sku', to='tyre.stuffing')),
                ('tyre_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku', to='tyre.tyreset')),
                ('tyre_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku', to='tyre.tyresize')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Advance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('percentage', models.FloatField()),
                ('remarks', models.TextField()),
                ('advance_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advance', to='process.advancetype')),
                ('quotaion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advance', to='process.quotation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
