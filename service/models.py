from django.db import models
from django.urls import reverse

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
        return reverse('service:sittings_by_city', args=[self.slug])
        
    def __str__(self):
        return '{}'.format(self.name)


class Nursery(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='nursery', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'nursery'
        verbose_name_plural = 'nurseries'
        
    def get_url(self):
        return reverse('service:SittingDetail', args=[self.city.slug, self.slug])
        
    def __str__(self):
        return '{}'.format(self.name)