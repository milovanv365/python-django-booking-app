# Generated by Django 2.2.2 on 2019-10-24 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0008_auto_20191025_0311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='price',
            new_name='amount',
        ),
    ]
