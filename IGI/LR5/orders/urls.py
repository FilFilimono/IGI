from django.urls import path, re_path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    re_path(r'^(?P<pk>\d+)/$', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.order_update, name='order_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.order_delete, name='order_delete'),
    path('statistics/', views.statistics, name='statistics'),
]
