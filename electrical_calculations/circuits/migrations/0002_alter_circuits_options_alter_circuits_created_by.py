# Generated by Django 5.1.3 on 2024-11-27 01:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circuits', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='circuits',
            options={'verbose_name': 'Circuit', 'verbose_name_plural': 'Circuits'},
        ),
        migrations.AlterField(
            model_name='circuits',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created', to=settings.AUTH_USER_MODEL),
        ),
    ]
