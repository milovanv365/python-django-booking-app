from django.urls import path
from . import views

app_name='reservation'

urlpatterns = [
     path('add/<int:nursery_id>/', views.add_reservation, name='add_reservation'),
     path('', views.reservation_detail, name='reservation_detail'), 
     path('remove/<int:nursery_id>/', views.reservation_remove, name='reservation_remove'),
     path('full_remove/<int:nursery_id>/', views.full_remove, name='full_remove'),
     path('new/', views.reservation_new, name='reservation_new'),
     path('thankyou/', views.thankyou, name='thankyou'),
]