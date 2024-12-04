# Generated by Django 5.1.3 on 2024-11-29 06:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circuits', '0002_alter_circuits_options_alter_circuits_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calculations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datas', models.JSONField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Calculation',
                'verbose_name_plural': 'Calculations',
            },
        ),
        migrations.DeleteModel(
            name='Circuits',
        ),
    ]
