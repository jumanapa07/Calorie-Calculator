# Generated by Django 4.2.6 on 2023-11-22 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CalorieCalc', '0010_alter_foodlog_quantity_alter_foodlog_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodlog',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=3, default=1, max_digits=7, null=True),
        ),
    ]
