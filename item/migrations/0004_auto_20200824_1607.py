# Generated by Django 3.1 on 2020-08-24 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_auto_20200820_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='receive',
            name='receive_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
