from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('add/<int:nursery_id>/', views.add_reservation, name='AddReservation'),
]
