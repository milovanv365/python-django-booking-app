from django.urls import path
from . import views

app_name='service'

urlpatterns = [
    path('', views.allCity, name='allCity'),
    path('<slug:c_slug>/',views.allSitting, name='sittings_by_city'),  
    path('<slug:c_slug>/<slug:nursery_slug>/', views.SittingDetail, name='SittingDetail'),
    path('howto/', views.index, name='index'),
]