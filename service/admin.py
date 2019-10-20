from django.contrib import admin
from .models import City,Nursery

class CityAdmin(admin.ModelAdmin):
    list_display = ['name','slug','description']
  #  list_editable = ['description']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(City,CityAdmin)

class NurseryAdmin(admin.ModelAdmin):
    list_display = ['name','description','price','stock','available']
    list_editable = ['stock','available']
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 20
admin.site.register(Nursery,NurseryAdmin)