from django.db import models
from django.contrib.auth.models import User
from service.models import Nursery


class Reservation(models.Model):
    start_date = models.DateField(blank=True)
    start_time = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    child_age = models.IntegerField()
    allergy = models.TextField(blank=True, null=True)
    vaccination = models.TextField(max_length=1000, blank=True, null=True)
    illness = models.TextField(blank=True, null=True)
    travel_insurance = models.TextField(blank=True, null=True)
    wifi = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    period = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Reservation'
        ordering = ['-created_at']

    def _str_(self):
        return self.name


class Payment(models.Model):
    token = models.CharField(max_length=250, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Total')
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=10, blank=True)
    billingCountry = models.CharField(max_length=200, blank=True)
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostcode = models.CharField(max_length=10, blank=True)
    shippingCountry = models.CharField(max_length=200, blank=True)

    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Payment'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)
