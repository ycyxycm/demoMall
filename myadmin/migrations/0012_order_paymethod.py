# Generated by Django 2.2.24 on 2021-12-18 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0011_order_orderinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paymethod',
            field=models.IntegerField(default=0),
        ),
    ]
