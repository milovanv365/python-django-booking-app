# Generated by Django 2.2.2 on 2019-10-30 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_nurserylimit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nurserylimit',
            name='nursery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Nursery'),
        ),
    ]
