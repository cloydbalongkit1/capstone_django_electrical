# Generated by Django 5.1.3 on 2024-12-11 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circuits', '0009_remove_calculations_data_calculation_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
            ],
        ),
    ]
