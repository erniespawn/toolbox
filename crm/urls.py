from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include

app_name = 'crm'


urlpatterns = [
    path('', views.cdr_detail_view, name='cdr_detail_view'),
    # path('reset/', views.reset, name="reset"),
    path('customer/', views.customer, name="customer"),
    path('smsc/', views.form_submit, name='form_submit'),
    path('esme_dlr/', views.esme_dlr, name='esme_dlr'),
    path('esme_dlr_view/', views.esme_dlr_view, name='esme_dlr_view'),
    path('sendSMS/', views.sendSMS, name='sendSMS'),
    path('sendSMS/<str:room_name>/', views.sendSMSroom, name='sendSMSroom'),
    path('chat_box/', views.chat_box, name='chat_box'),
    path('chat_box/<str:room_name>/', views.chatboxroom, name='chatboxroom'),
    path('fb/', views.fb, name='fb'),
    path('ss7hub/', views.ss7hub, name='ss7hub'),
    path('srilookup/', views.srilookup, name='srilookup'),
    path('newSG/', views.newSG, name='newSG'),
]
