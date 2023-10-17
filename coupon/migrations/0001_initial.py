# Generated by Django 4.2.4 on 2023-10-14 03:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(max_length=100)),
                ('coupon_code', models.CharField(max_length=100)),
                ('min_price', models.IntegerField()),
                ('coupon_discount_amount', models.PositiveIntegerField()),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
    ]
