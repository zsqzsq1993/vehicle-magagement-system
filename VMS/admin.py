from django.contrib.admin import ModelAdmin
from django.contrib import admin
from .models import Project, Vehiclecom, Vehiclestr, Logcom, Logstr
# Register your models here.
class ProjectAdmin(ModelAdmin):
    list_display = ('project_name', 'project_manager','project_principal')
    list_filter = ['project_principal']

class VehiclecomAdmin(ModelAdmin):
    list_display = ('project','vehicle_number','vehicle_cartype','vehicle_main','vehicle_totkilo','vehicle_process','vehicle_continue')
    list_filter = ['project']

class LogcomAdmin(ModelAdmin):
    list_display = ('log_pro_veh','log_cartype','log_date','log_name','log_kilotdy','log_worktime')
    list_filter = ['log_pro_veh']

class VehiclestrAdmin(ModelAdmin):
    list_display = ('project','vehicle_number','vehicle_cartype','vehicle_badroad','vehicle_process','vehicle_continue')
    list_filter = ['project']

class LogstrAdmin(ModelAdmin):
    list_display = ('log_pro_veh','log_cartype','log_date','log_name','log_kilotdy','log_worktime')
    list_filter = ['log_pro_veh']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Vehiclecom, VehiclecomAdmin)
admin.site.register(Logcom, LogcomAdmin)
admin.site.register(Vehiclestr, VehiclestrAdmin)
admin.site.register(Logstr, LogstrAdmin)

