# Generated by Django 4.0 on 2022-03-21 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rank',
            field=models.IntegerField(blank=True, default=100, null=True),
        ),
    ]
