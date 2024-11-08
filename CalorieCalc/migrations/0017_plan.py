# Generated by Django 4.2.6 on 2023-12-03 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CalorieCalc', '0016_rename_quantity_food_serving_size_food_cholestrol_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('current', models.PositiveIntegerField()),
                ('target', models.PositiveIntegerField()),
                ('duration', models.PositiveIntegerField()),
                ('calorie_needed', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weight_plan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
