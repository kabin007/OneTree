# Generated by Django 5.0.7 on 2024-07-24 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_cartitem_quantity_address_delete_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='ward',
        ),
    ]
