# Generated by Django 3.1 on 2020-09-17 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0010_auto_20200912_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='issue_type',
            field=models.CharField(default='direct', max_length=50),
        ),
    ]
