# Generated by Django 5.1.3 on 2024-11-29 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circuits', '0003_calculations_delete_circuits'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculations',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
