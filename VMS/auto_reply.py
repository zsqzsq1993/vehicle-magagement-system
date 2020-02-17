import re
import time
import hashlib
from lxml import etree
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse
from .models import Project, Vehiclecom, Vehiclestr
from .forms import *

def check(request):
    try:
        content = request.GET
        if len(content) == 0:
            response = '抱歉，您只能通过微信API来访问我。'
            return HttpResponse(response)
        signature = content['signature']
        timestamp = content['timestamp']
        nonce = content['nonce']
        echostr = content['echostr']
        token = "zsqzsq"

        lis = [token, timestamp, nonce]
        lis.sort()
        sha = hashlib.sha1()
        for i in range(3):
            sha.update(lis[i].encode("utf-8"))
        hascode = sha.hexdigest()
        if hascode == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('wrong')
    except Exception as e:
        return HttpResponse(e)

class Analyze:
    def __init__(self, request):
        str_xml  = etree.fromstring(request.body)
        self.fromUser       = str_xml.find('ToUserName').text
        self.toUser         = str_xml.find('FromUserName').text
        self.input_content  = str_xml.find('Content').text
        self.output_content = ''
        self.nowtime  = time.time()
        self.project = None
        self.vehicle = None

    def ret_template(self):
        if self.input_content.strip() in ['目录','0']:
            self.output_content = catalogue
            return True
        for i in range(5):
            if self.input_content.strip() == str(i+1):
                self.output_content = template[i]
                return True
        return False

    def branch1(self,log_project_name,log_vehicle_number,content_list,log_testtype='综合耐久'):
        #判断输入数量准确
        if len(content_list) != 15:
            self.output_content = '信息不完整，请重新填写。' + template6
            return
        log_project_name   = log_project_name.upper()
        log_vehicle_number = log_vehicle_number.upper()
        log_name       = content_list[3].split(':')[-1].strip()
        log_startkilo  = int(content_list[6].split(':')[-1].strip())
        log_endkilo    = int(content_list[7].split(':')[-1].strip())
        log_main       = int(content_list[8].split(':')[-1].strip())
        log_A          = int(content_list[9].split(':')[-1].strip())
        log_B          = int(content_list[10].split(':')[-1].strip())
        log_C          = int(content_list[11].split(':')[-1].strip())
        log_highspeed  = int(content_list[12].split(':')[-1].strip())
        log_normal     = int(content_list[13].split(':')[-1].strip())
        log_fuel       = int(content_list[14].split(':')[-1].strip())
        xs = []
        for x in content_list[4:6]:
            if len(re.findall(':',x))!=2:
                self.output_content = '时间格式错误，请重新填写。' + template6
                return
            xs.append(datetime.strptime(':'.join(x.split(':')[-2:]), '%H:%M'))
        log_startime   = xs[0]
        log_endtime    = xs[1]
        if int(log_endkilo) < int(log_startkilo):
            self.output_content = '当天里程出现错误，请重新填写。'+template6
            return
        log_bad        = int(log_endkilo)-int(log_startkilo)-int(log_normal)-int(log_highspeed)
        if log_bad < 0:
            self.output_content = '当天里程出现错误，请重新填写。'+template6
            return
        #录入系统
        newlog = self.vehicle.logcom_set.create(
        log_project     = log_project_name,
        log_vehicle     = log_vehicle_number,
        log_pro_veh     = '-'.join([log_project_name,log_vehicle_number]),
        log_testtype    = log_testtype,
        log_cartype     = self.vehicle.vehicle_cartype,
        log_name        = log_name,
        log_start_time  = log_startime,
        log_end_time    = log_endtime,
        log_start_kilo  = log_startkilo,
        log_end_kilo    = log_endkilo,
        log_main        = log_main,
        log_A           = log_A,
        log_B           = log_B,
        log_C           = log_C,
        log_highspeed   = log_highspeed,
        log_normal      = log_normal,
        log_badroad     = log_bad,
        log_fuel        = log_fuel,
        log_worktime    = log_endtime-log_startime,
        log_kilotdy     = log_endkilo-log_startkilo)
        self.vehicle.update(log_A,log_B, log_C, log_main, log_highspeed, log_normal, log_bad, log_fuel, ( log_highspeed+log_bad))

        newlog.save()
        self.vehicle.save()
        self.output_content = '日报录入成功，谢谢。'
        return

    def branch2(self,log_project_name,log_vehicle_number,content_list,log_testtype='高强耐久'):
        # 判断输入数量准确
        if len(content_list) != 10:
            self.output_content = '信息不完整，请重新填写。' + template6
            return
        log_project_name   = log_project_name.upper()
        log_vehicle_number = log_vehicle_number.upper()
        log_name           = content_list[3].split(':')[-1].strip()
        log_startkilo      = int(content_list[6].split(':')[-1].strip())
        log_endkilo        = int(content_list[7].split(':')[-1].strip())
        log_normal         = int(content_list[8].split(':')[-1].strip())
        log_fuel           = int(content_list[9].split(':')[-1].strip())
        xs = []
        for x in content_list[4:6]:
            if len(re.findall(':', x)) != 2:
                self.output_content = '时间格式错误，请重新填写。' + template6
                return
            xs.append(datetime.strptime(':'.join(x.split(':')[-2:]), '%H:%M'))
        log_startime = xs[0]
        log_endtime = xs[1]
        if int(log_endkilo) < int(log_startkilo):
            self.output_content = '当天里程出现错误，请重新填写。' + template6
            return
        log_bad = int(log_endkilo) - int(log_startkilo) - int(log_normal)
        if log_bad < 0:
            self.output_content = '当天里程出现错误，请重新填写。' + template6
            return
        # 录入系统
        newlog = self.vehicle.logstr_set.create(
            log_project    = log_project_name,
            log_vehicle    = log_vehicle_number,
            log_pro_veh    = '-'.join([log_project_name, log_vehicle_number]),
            log_testtype   = log_testtype,
            log_cartype    = self.vehicle.vehicle_cartype,
            log_name       = log_name,
            log_start_time = log_startime,
            log_end_time   = log_endtime,
            log_start_kilo = log_startkilo,
            log_end_kilo   = log_endkilo,
            log_normal     = log_normal,
            log_badroad    = log_bad,
            log_fuel       = log_fuel,
            log_worktime    = log_endtime-log_startime,
            log_kilotdy     = log_endkilo-log_startkilo)
        self.vehicle.update(log_normal,log_bad,log_fuel)
        newlog.save()
        self.output_content = '日报录入成功，谢谢。'
        self.vehicle.save()
        return
    def main_process(self):
        #判断索引索引页
        if self.ret_template(): return

        #获取关键list
        content_list = [x.strip() for x in self.input_content.split('\n')]
        for x in content_list:
            if x.split(':')[-1]=='':
                self.output_content = '不能留空，请重新填写。'+template6
                return
        #判断识别码
        log_code = content_list[0].split(':')[-1].strip()
        if log_code != passwd:
            self.output_content = '识别码错误，请重新填写。'+template6
            return

        #获取车辆&项目号：
        log_project_name   = content_list[1].split(':')[-1].strip()
        log_vehicle_number = content_list[2].split(':')[-1].strip()
        try:
            self.project = Project.objects.get(project_name= log_project_name)
        except (KeyError, Project.DoesNotExist):
            self.output_content = '项目号不存在，请重新录入或与工程师确认。' + template6
            self.project = None
            return
        try:
            self.vehicle = self.project.vehiclecom_set.get(vehicle_number= log_vehicle_number)
        except (KeyError, Vehiclecom.DoesNotExist):
            try:
                self.vehicle = self.project.vehiclestr_set.get(vehicle_number= log_vehicle_number)
            except (KeyError, Vehiclestr.DoesNotExist):
                self.output_content = '车辆号不存在，请重新录入或与工程师确认。' + template6
                self.vehicle = None
                return
        #获取项目类型并做分类处理
        log_testtype = self.vehicle.vehicle_testtype
        if log_testtype == '综合耐久':    self.branch1(log_project_name,log_vehicle_number,content_list)
        elif log_testtype == '高强耐久':  self.branch2(log_project_name,log_vehicle_number,content_list)


    def go(self):
        self.main_process()
        return HttpResponse(XmlForm.format(self.toUser, self.fromUser, self.nowtime, self.output_content))









