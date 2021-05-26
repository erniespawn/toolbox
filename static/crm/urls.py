from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include

app_name = 'crm'


urlpatterns = [
    path('', views.cdr_detail_view, name='cdr_detail_view'),
    path('reset/', views.reset, name="reset"),
    path('customer/', views.customer, name="customer"),
    # path('smsc/', views.smsc, name="smsc"),
    path('smsc/', views.form_submit, name='form_submit'),
    path('esme_dlr/', views.esme_dlr, name='esme_dlr'),
    path('esme_dlr_reset/', views.esme_dlr_reset, name='esme_dlr_reset'),
]
