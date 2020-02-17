from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Project(models.Model):
    project_name      = models.CharField('试验项目',max_length=10,blank=False)
    project_manager   = models.CharField('试验经理',max_length=10,blank=False)
    project_principal = models.CharField('试验技责人',max_length=10,blank=False)
    project_start     = models.DateField('项目开始日期',auto_now_add=True,blank=False)
    def __str__(self):
        return self.project_name
    class Meta:
        verbose_name = '项目管理'
        verbose_name_plural = '项目管理'


class Vehiclecom(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目名称',blank=False)
    vehicle_number    = models.CharField('项目车号',max_length=20,blank=False)
    vehicle_testtype  = models.CharField('项目类型',max_length=20,default='综合耐久',editable=False,blank=False)
    vehicle_cartype   = models.CharField('车型',max_length=20,default='电车',blank=True)#允许不选
    vehicle_startdate = models.DateField('开始日期',auto_now_add=True,blank=False)
    vehicle_continue  = models.BooleanField('是否正常开展',default= True,blank=False)
    vehicle_finished  = models.BooleanField('是否结束',default= False,blank=False)
    vehicle_main      = models.IntegerField('累计主循环',default=0,blank=False)
    vehicle_A         = models.IntegerField('累计A循环',default=0,blank=False)
    vehicle_B         = models.IntegerField('累计B循环',default=0,blank=False)
    vehicle_C         = models.IntegerField('累计C循环',default=0,blank=False)
    vehicle_highspeed = models.IntegerField('总高环里程(km)',default=0,blank=False)
    vehicle_normal    = models.IntegerField('总连接路里程(km)',default=0,blank=False)
    vehicle_badroad   = models.IntegerField('总坏路里程(km)',default=0,blank=False)
    vehicle_process   = models.IntegerField('进度(%)',default=0,blank=False)
    vehicle_fuel      = models.IntegerField('总能耗',default=0,blank=False)
    vehicle_totkilo   = models.IntegerField('耐久里程(km)',default=0,blank=False)

    class Meta:
        verbose_name = '综合耐久车辆管理'
        verbose_name_plural = '综合耐久车辆管理'
    def __str__(self):
        return self.vehicle_number

    def update(self,a,b,c,mainn,highspeed,normal,badroad,fuel,totalkillo):
        self.vehicle_main += mainn
        self.vehicle_A += a
        self.vehicle_B += b
        self.vehicle_C += c
        self.vehicle_highspeed += highspeed
        self.vehicle_normal += normal
        self.vehicle_badroad += badroad
        self.vehicle_fuel += fuel
        self.vehicle_process = round((self.vehicle_main / 308)*100)
        self.vehicle_totkilo += totalkillo

class Vehiclestr(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目名称',blank=False)
    vehicle_number    = models.CharField('项目车号',max_length=20,blank=False)
    vehicle_testtype  = models.CharField('项目类型',max_length=20,default='高强耐久',editable=False,blank=False)
    vehicle_cartype   = models.CharField('车型',max_length=20,default='电车',blank=True)#允许不选
    vehicle_startdate = models.DateField('开始日期',auto_now_add=True,blank=False)
    vehicle_continue  = models.BooleanField('是否正常开展',default= True,blank=False)
    vehicle_finished  = models.BooleanField('是否结束',default= False,blank=False)
    vehicle_fuel      = models.IntegerField('总能耗',default=0,blank=False)
    vehicle_process   = models.IntegerField('进度(%)',default=0,blank=False)
    vehicle_normal    = models.IntegerField('总连接路里程(km)',default=0,blank=False)
    vehicle_badroad   = models.IntegerField('耐久里程(km)',default=0,blank=False)
    class Meta:
        verbose_name = '高强耐久车辆管理'
        verbose_name_plural = '高强耐久车辆管理'
    def __str__(self):
        return self.vehicle_number

    def update(self,normal,badroad,fuel):
        self.vehicle_normal += normal
        self.vehicle_badroad += badroad
        self.vehicle_fuel += fuel
        self.vehicle_process = round((self.vehicle_badroad / 7000)*100)

class Logcom(models.Model):
    log_project     = models.CharField('项目名',max_length=20,blank=False)
    log_vehicle     = models.CharField('车号',max_length=20,blank=False)
    log_pro_veh     = models.CharField('项目车号',max_length=20,blank=False)
    log_vehiclelink = models.ForeignKey(Vehiclecom, on_delete=models.CASCADE, verbose_name='关联车号')
    log_testtype    = models.CharField('项目类型',max_length=20,default='综合耐久',editable=False)
    log_cartype     = models.CharField('车型(填电车或油车)',max_length=20,blank=False)
    log_name        = models.CharField('驾驶员姓名',max_length=20,blank=False)
    log_date        = models.DateField('日期',auto_now=True)
    log_start_time  = models.TimeField('开始时间',blank=False)
    log_end_time    = models.TimeField('结束时间',blank=False)
    log_start_kilo  = models.IntegerField('开始里程',blank=False)
    log_end_kilo    = models.IntegerField('结束里程',blank=False)
    log_main        = models.IntegerField('主循环',default=0,blank=False)
    log_A           = models.IntegerField('A循环',default=0,blank=False)
    log_B           = models.IntegerField('B循环',default=0,blank=False)
    log_C           = models.IntegerField('C循环',default=0,blank=False)
    log_highspeed   = models.IntegerField('高环里程(km)',default=0,blank=False)
    log_normal      = models.IntegerField('连接路里程(km)',default=0,blank=False)
    log_badroad     = models.IntegerField('坏路里程(km)',default=0,blank=False)
    log_fuel        = models.IntegerField('该班能耗量',blank=False)
    log_worktime    = models.DurationField('工作时长',blank=False)
    log_kilotdy      = models.IntegerField('当班里程',blank=False)

    class Meta:
        verbose_name = '综合耐久日志管理'
        verbose_name_plural = '综合耐久日志管理'

class Logstr(models.Model):
    log_project     = models.CharField('项目名',max_length=20,blank=False)
    log_vehicle     = models.CharField('车号',max_length=20,blank=False)
    log_pro_veh     = models.CharField('项目车号',max_length=20,blank=False)
    log_vehiclelink = models.ForeignKey(Vehiclestr, on_delete=models.CASCADE, verbose_name='关联车号')
    log_testtype    = models.CharField('项目类型',max_length=20,default='高强耐久',editable=False)
    log_cartype     = models.CharField('车型(填电车或油车)',max_length=20,blank=False)
    log_name        = models.CharField('驾驶员姓名',max_length=20,blank=False)
    log_date        = models.DateField('日期',auto_now=True)
    log_start_time  = models.TimeField('开始时间',blank=False)
    log_end_time    = models.TimeField('结束时间',blank=False)
    log_start_kilo  = models.IntegerField('开始里程',blank=False)
    log_end_kilo    = models.IntegerField('结束里程',blank=False)
    log_normal      = models.IntegerField('连接路里程(km)',default=0,blank=False)
    log_badroad     = models.IntegerField('坏路里程(km)',default=0,blank=False)
    log_fuel        = models.IntegerField('该班能耗量',blank=False)
    log_worktime    = models.DurationField('工作时长',blank=False)
    log_kilotdy      = models.IntegerField('当班里程',blank=False)

    class Meta:
        verbose_name = '高强耐久日志管理'
        verbose_name_plural = '高强耐久日志管理'






