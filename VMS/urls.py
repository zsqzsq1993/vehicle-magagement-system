from django.urls import path
from . import views
app_name = 'VMS'
urlpatterns = [
    path('', views.VMS.as_view(), name='VMS')
]