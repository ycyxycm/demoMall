# Generated by Django 2.2.24 on 2021-12-18 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0009_shoppingcart'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recename', models.CharField(max_length=30)),
                ('recephone', models.CharField(max_length=11)),
                ('receaddress', models.CharField(max_length=100)),
                ('receselect', models.IntegerField(default=0)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Users')),
            ],
        ),
    ]