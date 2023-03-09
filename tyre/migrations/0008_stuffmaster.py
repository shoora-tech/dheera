# Generated by Django 3.2.18 on 2023-03-08 15:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tyre', '0007_auto_20230307_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='StuffMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stuff', models.FloatField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuff_master', to='tyre.brand')),
                ('container_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuff_master', to='tyre.containertype')),
                ('pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuff_master', to='tyre.pattern')),
                ('pr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuff_master', to='tyre.pr')),
                ('tyre_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuff_master', to='tyre.tyresize')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]