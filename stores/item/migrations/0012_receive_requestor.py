# Generated by Django 3.1 on 2020-10-13 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0011_issue_issue_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='receive',
            name='requestor',
            field=models.CharField(default='Brian', max_length=100),
            preserve_default=False,
        ),
    ]
