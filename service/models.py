from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='city', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def get_url(self):
        return reverse('service:CityDetail', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)


class Nursery(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    price_plan = models.TextField(blank=True)
    stock = models.IntegerField()
    description = models.TextField(blank=True)
    address = models.CharField(max_length=250, blank=True)
    telephone = models.CharField(max_length=250, blank=True)
    station = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='nursery', blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'nursery'
        verbose_name_plural = 'nurseries'

    def get_url(self):
        return reverse('service:NurseryDetail', args=[self.city.slug, self.slug])

    def __str__(self):
        return '{}'.format(self.name)


class NurseryLimit(models.Model):
    date = models.DateField()
    time_from = models.IntegerField()
    time_to = models.IntegerField()
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'nursery_limit'
        ordering = ['date']

    def _str_(self):
        return self.date
