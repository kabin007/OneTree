# Generated by Django 5.0.7 on 2024-07-24 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_address_ward'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='ward',
            field=models.CharField(default='Mechinagar-9', max_length=100),
        ),
    ]