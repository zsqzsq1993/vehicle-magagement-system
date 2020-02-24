from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View, generic
from .auto_reply import check, Analyze
from .models import Vehiclecom, Vehiclestr, Logcom, Logstr
from django.contrib.auth import authenticate
from django.contrib.auth import login as lgin, logout as lgout
from django.contrib.auth.decorators import login_required
import csv,codecs

# Create your views here.
class WeChat(View):
    def get(self,request):
        response = check(request)
        return response

    def post(self,request):
        analysis = Analyze(request)
        response = analysis.go()
        return response

def index(request):
    if not request.user.is_authenticated:
        return redirect('VMS:login')
    else:
        vehiclecom_list = Vehiclecom.objects.order_by('-project')
        vehiclestr_list = Vehiclestr.objects.order_by('-project')
        num = vehiclecom_list.count()
        context = {
            'vehiclecom_list': vehiclecom_list,
            'vehiclestr_list': vehiclestr_list,
            'num': num,
            'username':request.user.username.upper(),
        }
        return render(request, 'VMS/index.html', context)

def logcom(request, vehicle_id):
    if not request.user.is_authenticated:
        return redirect('VMS:login')
    vehicle = get_object_or_404(Vehiclecom, pk= vehicle_id)
    logcom_list = vehicle.logcom_set.order_by('-log_date','-log_start_time')
    print(logcom_list)
    context = {
        'logcom_list': logcom_list,
        'vehicle':vehicle,
        'username': request.user.username.upper(),
    }
    return render(request, 'VMS/logcom.html',context)

def logstr(request, vehicle_id):
    if not request.user.is_authenticated:
        return redirect('VMS:login')
    vehicle = get_object_or_404(Vehiclestr, pk= vehicle_id)
    logstr_list = vehicle.logstr_set.order_by('-log_date','-log_start_time')
    context = {
        'longstr_list': logstr_list,
        'vehicle':vehicle,
        'username': request.user.username.upper(),
    }
    return render(request, 'VMS/logstr.html',context)

def login(request):
    lgout(request)
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('passwd', None)
        user = authenticate(request, username=username, password=password)
        if user:
            lgin(request, user)
            return redirect('VMS:index')
        else:
            return render(request, 'VMS/login.html')
    else:
        return render(request, 'VMS/login.html')

def logout(request):
    lgout(request)
    return redirect('VMS:index')

def downloadcom(request,vehicle_id):
    if not request.user.is_authenticated:
        return redirect('VMS:login')
    vehicle = get_object_or_404(Vehiclecom, pk= vehicle_id)
    logcom_list = vehicle.logcom_set.order_by('-log_date','-log_start_time')

    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] =  'attachment;filename="%s.csv"' % '-'.join([str(vehicle.project), vehicle.vehicle_number])
    writer = csv.writer(response)
    first_row = ['项目名称','车辆编号','项目类型','车辆类型','累计主循环','累计A','累计B','累计C','累计坏路','累计高环','累计能耗']
    writer.writerow(first_row)
    writer.writerow([vehicle.project,vehicle.vehicle_number,vehicle.vehicle_testtype,vehicle.vehicle_cartype,vehicle.vehicle_main,
                     vehicle.vehicle_A,vehicle.vehicle_B,vehicle.vehicle_C,vehicle.vehicle_badroad,vehicle.vehicle_highspeed,vehicle.vehicle_fuel])
    writer.writerow([]); writer.writerow([])
    writer.writerow(['日期','驾驶员','上班时间','下班时间','上车里程','下车里程','主循环','A循环','B循环','C循环','高环里程','坏路里程','连接路里程','能耗'])
    for log in logcom_list:
        writer.writerow([log.log_date,log.log_name,log.log_start_time,log.log_end_time,log.log_start_kilo,log.log_end_kilo,log.log_main,
                         log.log_A,log.log_B,log.log_C,log.log_highspeed,log.log_badroad,log.log_normal,log.log_fuel])
    return response

def downloadstr(request,vehicle_id):
    if not request.user.is_authenticated:
        return redirect('VMS:login')
    vehicle = get_object_or_404(Vehiclestr, pk= vehicle_id)
    logstr_list = vehicle.logstr_set.order_by('-log_date','-log_start_time')

    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] =  'attachment;filename="%s.csv"' % '-'.join([str(vehicle.project), vehicle.vehicle_number])
    writer = csv.writer(response)
    first_row = ['项目名称','车辆编号','项目类型','车辆类型','累计坏路','累计能耗']
    writer.writerow(first_row)
    writer.writerow([vehicle.project,vehicle.vehicle_number,vehicle.vehicle_testtype,vehicle.vehicle_cartype,
                     vehicle.vehicle_badroad,vehicle.vehicle_fuel])
    writer.writerow([]); writer.writerow([])
    writer.writerow(['日期','驾驶员','上班时间','下班时间','上车里程','下车里程','连接路里程','坏路里程','能耗'])
    for log in logstr_list:
        writer.writerow([log.log_date,log.log_name,log.log_start_time,log.log_end_time,log.log_start_kilo,log.log_end_kilo,
                         log.log_normal,log.log_badroad,log.log_fuel])
    return response



