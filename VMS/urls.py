from django.urls import path
from . import views
app_name = 'VMS'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.login, name='logout'),
    path('WeChat/', views.WeChat.as_view(), name='wechat'),
    path('index/', views.index, name='index'),
    path('logcom/<int:vehicle_id>',views.logcom, name='logcom'),
    path('logstr/<int:vehicle_id>',views.logstr, name='logstr'),
]