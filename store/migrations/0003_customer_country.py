# Generated by Django 4.0 on 2022-02-21 03:07

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='country',
            field=django_countries.fields.CountryField(default='United States', max_length=2),
        ),
    ]
