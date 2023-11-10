# Generated by Django 4.2.4 on 2023-11-10 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_alter_order_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(blank=True, max_length=50)),
                ('state', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('pincode', models.CharField(blank=True, max_length=50)),
                ('order_note', models.CharField(blank=True, max_length=100, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.order')),
            ],
        ),
    ]
