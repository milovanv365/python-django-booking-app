# Generated by Django 2.2.2 on 2019-10-23 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nursery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True)),
                ('address', models.CharField(blank=True, max_length=250)),
                ('telephone', models.CharField(blank=True, max_length=250)),
                ('station', models.CharField(blank=True, max_length=250)),
                ('price_plan', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='nursery')),
                ('stock', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.City')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'nursery',
                'verbose_name_plural': 'nurseries',
                'ordering': ('name',),
            },
        ),
    ]
