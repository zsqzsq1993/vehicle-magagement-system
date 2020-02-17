from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .auto_reply import check, Analyze

# Create your views here.
class VMS(View):
    def get(self,request):
        response = check(request)
        return response

    def post(self,request):
        analysis = Analyze(request)
        response = analysis.go()
        return response



