# Generated by Django 3.1 on 2020-08-30 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0007_item_item_sage_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='recent',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='item',
            name='reorder_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('in stock', 'primary'), ('out of stock', 'danger'), ('reorder now', 'warning')], default='in stock', max_length=50),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='shelf_lbl',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='item.shelf'),
        ),
    ]