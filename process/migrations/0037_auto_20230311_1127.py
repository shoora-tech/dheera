# Generated by Django 3.2.18 on 2023-03-11 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tyre', '0008_stuffmaster'),
        ('process', '0036_auto_20230311_1116'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContainerManagement',
            new_name='ContainerSKU',
        ),
        migrations.RemoveField(
            model_name='containersku',
            name='bl',
        ),
        migrations.AddField(
            model_name='containersku',
            name='box',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cm_sku', to='process.containerbox'),
        ),
    ]
