# Generated by Django 2.2.2 on 2019-10-29 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0011_auto_20191026_0344'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='child_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='child_age',
            field=models.IntegerField(default=0),
        ),
    ]