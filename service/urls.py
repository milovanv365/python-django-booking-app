from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.all_city, name='AllCity'),
    path('<slug:c_slug>/', views.city_detail, name='CityDetail'),
    path('<slug:c_slug>/<slug:nursery_slug>/', views.nursery_detail, name='NurseryDetail'),
    path('howto/', views.index, name='index'),
    path('vendor/dashboard/nursery/add', views.vendor_dashboard, name='VendorDashboard'),
    path('vendor/dashboard/nursery/limit/list', views.vendor_nursery_limit_list, name='VendorNurseryLimitList'),
    path('vendor/dashboard/nursery/limit/add', views.vendor_nursery_limit_add, name='VendorNurseryLimitAdd'),
    path('vendor/dashboard/nursery/limit/edit/<int:limit_id>', views.vendor_nursery_limit_edit, name='VendorNurseryLimitEdit'),
    path('vendor/dashboard/nursery/limit/delete/<int:limit_id>', views.vendor_nursery_limit_delete, name='VendorNurseryLimitDelete'),
]
