# Generated by Django 2.2.2 on 2019-11-01 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0014_auto_20191101_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='price',
            new_name='price_plan',
        ),
        migrations.AddField(
            model_name='reservation',
            name='price_total',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
