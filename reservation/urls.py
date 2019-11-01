from django.urls import path
from . import views

app_name = 'reservation'


urlpatterns = [
    path('add/<int:nursery_id>', views.reservation_add, name='ReservationAdd'),
    path('edit/<int:reservation_id>', views.reservation_edit, name='ReservationEdit'),
    path('transaction/<int:reservation_id>', views.reservation_transaction, name='ReservationConfirm'),
    path('completed/<int:reservation_id>', views.reservation_completed, name='ReservationCompleted'),
    path('history/list', views.history_list, name='ReservationHistoryList'),
    path('detail/<int:reservation_id>', views.history_detail, name='ReservationDetail'),
    path('history/delete/<int:reservation_id>', views.history_delete, name='ReservationHistoryDelete'),
    path('add/ajax/stock_per_date', views.get_stock_per_date),
    path('add/ajax/available-time-per-date', views.get_available_time_per_date),
    path('edit/ajax/stock_per_date', views.get_stock_per_date),
    path('edit/ajax/available-time-per-date', views.get_available_time_per_date)
]
