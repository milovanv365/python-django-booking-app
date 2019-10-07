from django.db import models
from service.models import Nursery

class Reservation(models.Model):
    reservation_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'Reservation'
        ordering = ['date_added']
        
    def __str__(self):
        return self.reservation_id

    
class ReservationItem(models.Model):
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)
    class Meta:
        db_table = 'ReservationItem'
        
    def sub_total(self):
        return self.nursery.price * self.quantity
    
    def __str__(self):
        return self.nursery
    
class ReservationInfomation(models.Model):
    TIME_CHOICES = (
        ('10:00-17:00', '10:00-17:00'),
        ('9:00-13:00', '9:00-13:00'),
        ('13:00-17:00', '13:00-17:00'),
        ('17:00-21:00', '17:00-21:00'),
    )
    rtime = models.CharField(max_length=20, choices=TIME_CHOICES)
    your_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    reservation_date = models.DateField()
    age_ofthechild = models.CharField(max_length=200)
    allergies = models.TextField(max_length=2000, blank=True, null=True)
    vaccinations = models.CharField(max_length=1000, blank=True, null=True)
    illness = models.CharField(max_length=1000, blank=True, null=True)
    travel_insurance = models.CharField(max_length=1000, blank=True, null=True)
    wifi = models.CharField(max_length=1000, blank=True, null=True)
    note = models.TextField(max_length=2000, blank=True, null=True)
    
    def _str_(self):
        return self.your_name
    