# Generated by Django 2.2.2 on 2019-10-30 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0003_auto_20191025_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='NurseryLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_from', models.IntegerField()),
                ('time_to', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nursery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nursery_limit',
                'ordering': ['date'],
            },
        ),
    ]