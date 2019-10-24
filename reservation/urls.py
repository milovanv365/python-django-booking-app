from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('add/<int:nursery_id>', views.reservation_add, name='ReservationAdd'),
    path('transaction/<int:reservation_id>', views.reservation_transaction, name='ReservationConfirm')
]
