from django.urls import path, re_path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    re_path(r'^(?P<pk>\d+)/$', views.employee_detail, name='employee_detail'),
    path('create/', views.employee_create, name='employee_create'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.employee_update, name='employee_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.employee_delete, name='employee_delete'),
]
