from django.contrib import admin
from .models import ReservationInfomation

class ReservationInfomationAdmin(admin.ModelAdmin):
 #   model = ReservationInfomation
 #  fieldsets = [
 #    ('RTIME',{'fields':['rtime'],}),
 #   ('YOUR_NAME',{'fields':['your_name'],}),
 #   ('EMAIL',{'fields':['email'],}),      
 #   ]
 #    readonly_fields = ['nursery','quantity','price']
 #   can_delete= False
 #   max_num = 0
 #  template = 'admin/order/tabular.html'
    
    list_display = ['rtime','your_name','email','reservation_date','age_ofthechild','allergies','vaccinations','illness','travel_insurance','wifi','note']
#    list_editable = ['stock','available']
  #  prepopulated_fields = {'slug':('name',)}
    list_per_page = 20
admin.site.register(ReservationInfomation,ReservationInfomationAdmin)
