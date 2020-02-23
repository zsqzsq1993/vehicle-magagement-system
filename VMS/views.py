from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View, generic
from .auto_reply import check, Analyze
from .models import Vehiclecom, Vehiclestr, Logcom, Logstr
from django.contrib.auth import authenticate
from django.contrib.auth import login as lgin, logout as lgout
from django.contrib.auth.decorators import login_required

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
    logcom_list = vehicle.logcom_set.all()#order_by('-log_date','-log_start_time')
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




