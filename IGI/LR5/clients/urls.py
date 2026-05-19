from django.urls import path, re_path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client_list, name='client_list'),
    re_path(r'^(?P<pk>\d+)/$', views.client_detail, name='client_detail'),
    path('create/', views.client_create, name='client_create'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.client_update, name='client_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.client_delete, name='client_delete'),
]
