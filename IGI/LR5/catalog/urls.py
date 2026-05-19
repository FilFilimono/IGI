from django.urls import path, re_path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('categories/', views.category_list, name='category_list'),
    re_path(r'^item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    path('item/create/', views.item_create, name='item_create'),
    re_path(r'^item/(?P<pk>\d+)/edit/$', views.item_update, name='item_update'),
    re_path(r'^item/(?P<pk>\d+)/delete/$', views.item_delete, name='item_delete'),
    path('promos/', views.promo_list, name='promo_list'),
]
