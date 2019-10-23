from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.all_city, name='AllCity'),
    path('<slug:c_slug>/', views.city_detail, name='CityDetail'),
    path('<slug:c_slug>/<slug:nursery_slug>/', views.nursery_detail, name='NurseryDetail'),
    path('vendor/dashboard', views.vendor_dashboard, name='VendorDashboard'),
    path('howto/', views.index, name='index'),
]