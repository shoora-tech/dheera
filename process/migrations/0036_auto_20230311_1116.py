# Generated by Django 3.2.18 on 2023-03-11 11:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tyre', '0008_stuffmaster'),
        ('process', '0035_auto_20230311_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContainerBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='container_box', to='process.bl')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]