from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import CdrProcess, EsmeDlr
import subprocess, logging
from datetime import date, timedelta
from subprocess import PIPE, Popen
from django.db.models import Q
from crm.models import CdrProcess, row1_1, cdrTable
import sqlite3
from itertools import product
logger = logging.getLogger(__name__)
import datetime, os
from datetime import datetime, timedelta, date



def home(request):
    success_min0_smsc_2_eu4 = CdrProcess.objects.filter(status__exact="success").count()

    context = {
        'success_min0_smsc_2_eu4' : success_min0_smsc_2_eu4,
    }
    return render(request, "crm/dashboard.html", context)

def esme_dlr_view(request):
    return render(request, "crm/esme_dlr_reset.html", {})


def chat_box(request):
    return render(request, 'crm/chat_box.html', {})

def chatboxroom(request, room_name):
    return render(request, 'crm/chatboxroom.html', {
        'room_name': room_name
    })

def customer(request):
    return render(request, 'crm/customer.html')

def smsc(request):
    return render(request, 'crm/smsc.html')

def sendSMS(request):
    return render(request, 'crm/sendSMS.html', {})

def sendSMSroom(request, room_name):
    return render(request, 'crm/sendSMSroom.html', {
        'room_name': room_name
    })

def ss7hub(request):
    return render(request, 'crm/ss7hub.html', {})

def srilookup(request):
    return render(request, 'crm/srilookup.html', {})


def esme_dlr(request):
    print(request.POST)
    if request.method == 'POST':
        if request.POST.get("reset") == 'Reset':
            reset = request.POST.get("reset")
            EsmeDlr.objects.all().delete()   # Delete records from DB

            return render(request, "crm/esme_dlr.html", {})

        else:
            my_new_date = request.POST.get("date")
            my_new_smsc = request.POST.get("smsc")
            if my_new_date == '0':
                today = (date.today() - timedelta(days=0)).strftime('%m-%d')
                p = Popen(["ssh","{}".format(my_new_smsc),"python","/home/kennyC/sms/smsc_dlr_v1.py","-s","{}".format(my_new_date)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output, errors = p.communicate()
                # print (output)
                try:

                    list = []
                    st = " ".join(output.split('\n'))
                    st = st.split(' ')
                    x = EsmeDlr.objects.all()
                    print (x)

                    it = iter(st) #https://stackoverflow.com/questions/16789776/iterating-over-two-values-of-a-list-at-a-time-in-python
                    for a, b, c, d, e, f, g, h in zip(*[iter(it)]*8):
                        print (a, b, c, d, e, f, g, h)
                        p = EsmeDlr(
                        date="{}".format(a),
                        time="{}".format(b),
                        networkid="{}".format(c),
                        senderid="{}".format(d),
                        msisdn="{}".format(e),
                        status="{}".format(f),
                        messageid="{}".format(g),
                        system="{}".format(h),
                        )
                        p.save()
                except:
                    pass

            elif my_new_date == '-1':
                p = Popen(["ssh","{}".format(my_new_smsc),"python","/home/kennyC/sms/smsc_dlr_v1.py","-s","{}".format(my_new_date)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                output, errors = p.communicate()
                print (output)
                try:

                    list = []
                    st = " ".join(output.split('\n'))
                    st = st.split(' ')
                    x = EsmeDlr.objects.all()
                    print (x)

                    it = iter(st) #https://stackoverflow.com/questions/16789776/iterating-over-two-values-of-a-list-at-a-time-in-python
                    for a, b, c, d, e, f, g, h in zip(*[iter(it)]*8):
                        print (a, b, c, d, e, f, g, h)
                        p = EsmeDlr(
                        date="{}".format(a),
                        time="{}".format(b),
                        networkid="{}".format(c),
                        senderid="{}".format(d),
                        msisdn="{}".format(e),
                        status="{}".format(f),
                        messageid="{}".format(g),
                        system="{}".format(h),
                        )
                        p.save()
                except:
                    pass

            elif my_new_date == 'examplefile':
                today = (date.today() - timedelta(days=0)).strftime('%m-%d')
                p = Popen(["ssh","{}".format(my_new_smsc),"python","/home/kennyC/sms/smsc_dlr_v1.py","-s","{}".format(my_new_date)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output, errors = p.communicate()
                print (output)
                try:

                    list = []
                    st = " ".join(output.split('\n'))
                    st = st.split(' ')
                    x = EsmeDlr.objects.all()
                    print (x)

                    it = iter(st) #https://stackoverflow.com/questions/16789776/iterating-over-two-values-of-a-list-at-a-time-in-python
                    for a, b, c, d, e, f, g, h in zip(*[iter(it)]*8):
                        print (a, b, c, d, e, f, g, h)
                        p = EsmeDlr(
                        date="{}".format(a),
                        time="{}".format(b),
                        networkid="{}".format(c),
                        senderid="{}".format(d),
                        msisdn="{}".format(e),
                        status="{}".format(f),
                        messageid="{}".format(g),
                        system="{}".format(h),
                        )
                        p.save()
                except:
                    pass

            else:
                pass

    total_dbs_count = EsmeDlr.objects.filter(msisdn__startswith="65", status__exact="temp_failed_esme", senderid__exact="DBS_Bank").count()
    total_dbs = EsmeDlr.objects.filter(msisdn__startswith="65", status__exact="temp_failed_esme", senderid__exact="DBS_Bank")
    total_sg_count = EsmeDlr.objects.filter(msisdn__startswith="65", status__exact="temp_failed_esme").count()
    total_sg = EsmeDlr.objects.filter(msisdn__startswith="65", status__exact="temp_failed_esme")
    total_dlr_count = EsmeDlr.objects.filter(status__exact="temp_failed_esme").count()


    context={
        'total_dbs_count' : total_dbs_count,
        'total_dbs' : total_dbs,
        'total_sg_count' : total_sg_count,
        'total_sg' : total_sg,
        'total_dlr_count' : total_dlr_count,

        }

    return render(request, 'crm/esme_dlr.html', context)







def form_submit(request):
    print(request.POST)
    if request.method == 'POST':
        if request.POST.get("reset") == 'Reset':
            reset = request.POST.get("reset")
            print (reset)
            CdrProcess.objects.all().delete()   # Delete records from DB
            row1_1.objects.all().delete()       # Delete records from row1_1
            cdrTable.objects.all().delete()       # Delete records from cdrtable
            q = CdrProcess(time="00:00:00.000,", date='1999-99-99', msisdn='9999') # Insert 1 default record in DB and save it
            q.save()


            return render(request, "crm/smsc.html", {})

        # elif request.POST.get("insertDB") == 'insertDB':
        #     insertDB = request.POST.get("insertDB")
        #     con = sqlite3.connect('db.sqlite3')
        #     cur = con.cursor()
        #
        #     # DB_mode
        #     insert = 'insert'
        #     update = 'update'
        #     updateMtFailed = 'updateMtFailed'
        #     updateMtFwFailed = 'updateMtFwFailed'
        #     updateMtFailure = 'updateMtFailure'
        #     insertSriFB = 'insertSriFB'
        #     insertMtFB = 'insertMtFB'
        #     updateMtFB = 'updateMtFB'
        #     insertmt = 'insertmt'
        #     updateSuc = 'updateSuc'
        #     updateFail = 'updateFail'
        #     insertsgsrito = 'insertsgsrito'
        #     insertSriTimeOut = 'insertSriTimeOut'
        #     insertMtFail = 'insertMtFail'
        #     updateMtFail = 'updateMtFail'
        #     updateSriTimeOut = 'updateSriTimeOut'
        #     insertMtTimeOut = 'insertMtTimeOut'
        #     updateMtSysFail = 'updateMtSysFail'
        #
        #     insert1gt = 'insert1gt'
        #     insert2gt = 'insert2gt'
        #
        #
        #     ccsg = '65'
        #     ccms = '91'
        #     ccfb = '91'
        #
        #     gt_sg = '3197015001050,', '61491500050,'
        #     gt_sg1 = '3197015001050,'
        #     gt_sg2 = '61491500050,'
        #
        #     gt_6995 = '3197015001050,'
        #     gt_6994 = '3197015001052,'
        #     gt_6908 = '3197015001051,'
        #     gt_6909 = '3197015001053,'
        #     gt_dummy = 'dummy'
        #
        #     smsc = 'smsc-1-eu1,', 'smsc-2-eu1,', 'smsc-1-eu4,', 'smsc-2-eu4,'
        #     smsc1 = 'smsc-1-eu1,'
        #     smsc2 = 'smsc-2-eu1,'
        #     smsc3 = 'smsc-1-eu4,'
        #     smsc4 = 'smsc-2-eu4,'
        #     smscDummy = 'smscDummy'
        #
        #     system1 = 'smsc-1-eu1,'
        #     system2 = 'smsc-2-eu1,'
        #     system3 = 'smsc-1-eu4,'
        #     system4 = 'smsc-2-eu4,'
        #     system5 = 'smsc-1-eu1,', 'smsc-2-eu1,', 'smsc-1-eu4,', 'smsc-2-eu4,'
        #     system6 = 'smsc-2-eu4,', 'smsc-2-eu4,', 'smsc-2-eu4,', 'smsc-2-eu4,'
        #     system7 = 'smsc-2-eu1,', 'smsc-2-eu1,', 'smsc-2-eu1,', 'smsc-2-eu1,'
        #
        #     systemDummy = 'dummy'
        #
        #     success = 'success,'
        #     partial = 'partial,'
        #     failed = 'failed,'
        #     temp_failed = 'temp_failed,'
        #
        #     statTotal = """'failed,', 'success,', 'temp_failed,'"""
        #     statSuccess = """'success,'"""
        #     statFailed = """'failed,', 'temp_failed,'"""
        #
        #     statusTotal = 'failed,', 'success,', 'temp_failed,'
        #     statusSuccess = 'success,', 'dummy', 'dummy'        #2x dummy
        #     statusFailed = 'failed,', 'temp_failed,', 'dummy'   #1x dummy
        #     statusDummy = 'dummy', 'dummy', 'dummy'             #3x dummy
        #
        #     imsi1 = '52501'
        #     imsi2 = '52503'
        #     imsi3 = '52505'
        #     imsi7 = '4058'
        #     imsiDummy = 'dummy'
        #
        #
        #     tata = 'tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,'
        #     ibasis = 'ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,', 'ibasisc01,'
        #     comfone = 'comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,'
        #     bics = 'bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,', 'bicsc01,'
        #
        #     networkidTATA = 'tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,'
        #     networkidibasis = 'ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,', 'ibasisc01,'
        #     networkidComfone = 'comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,'
        #     networkidBics = 'bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,', 'bicsc01,'
        #     networkidDummy = 'dummy'
        #
        #     gtsg = '3197015001050,', '61491500050,'
        #     gtsg1 = '3197015001050,', '3197015001050,'
        #     gtsg2 = '61491500050,', '61491500050,'
        #
        #     gt6995 = '3197015001050,', '3197015001050,'
        #     gt6994 = '3197015001052,', '3197015001052,'
        #     gt6908 = '3197015001051,', '3197015001051,'
        #     gt6909 = '3197015001053,', '3197015001053,'
        #
        #     error_msg = 'error_msg'
        #
        #     db_err_field = 'db_err_field'
        #
        #     s1 = list2hourv2()
        #     print ("effe testen {}".format(s1))
        #
        #     r1 = list2hourv2()
        #     for x in r1:
        #         # Row 1
        #         r2 = ("{}:{}".format(x[0], x[1]))
        #         print (r2)
        #
        #         # Row 1 column 1 for Generic total, success, failed v3
        #         GenericTotal(insert, gtsg, r2, ccsg, statusTotal, db_err_field, systemDummy, imsiDummy, networkidDummy, error_msg, 'sg_10')
        #         GenericTotal(updateSuc, gtsg, r2, ccsg, statusSuccess, 'success', systemDummy, imsiDummy, networkidDummy, error_msg, 'sg_10')
        #         GenericTotal(updateFail, gtsg, r2, ccsg, statusFailed, 'failed1', systemDummy, imsiDummy, networkidDummy, error_msg, 'sg_10')
        #
        #         # Row 1 column 2 All MNO SRI timeouts
        #         GenericTotal(updateMtFailed, gtsg, r2, ccsg, statusDummy, 'failed2', systemDummy, imsiDummy, networkidDummy, 'onDialogTimeoutafterSRIRequest', 'sg_10')
        #
        #         # Row 1 column 3 fwsm timeout and SystemFailed for SingTel
        #         GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi1, networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_10')
        #         GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi1, networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_10')
        #
        #         # Row 1 column 3 fwsm timeout and SystemFailed for M1
        #         GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi2, networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_10')
        #         GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi2, networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_10')
        #
        #         # Row 1 column 3 fwsm timeout and SystemFailed for StarHub
        #         GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi3, networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_10')
        #         GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi3, networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_10')
        #
        #         # Row 2 -- SRI timeout -- GT 3197015001050 -- 1 Insert, 3 Update
        #         GenericTotal(insertSriTimeOut, gtsg1, r2, ccsg, statusDummy, 'failed1', systemDummy, imsiDummy, networkidTATA, 'onDialogTimeoutafterSRIRequest', 'sg_11')
        #         GenericTotal(updateSriTimeOut, gtsg1, r2, ccsg, statusDummy, 'failed2', systemDummy, imsiDummy, networkidibasis, 'onDialogTimeoutafterSRIRequest', 'sg_11')
        #         GenericTotal(updateSriTimeOut, gtsg1, r2, ccsg, statusDummy, 'failed3', systemDummy, imsiDummy, networkidComfone, 'onDialogTimeoutafterSRIRequest', 'sg_11')
        #         GenericTotal(updateSriTimeOut, gtsg1, r2, ccsg, statusDummy, 'failed4', systemDummy, imsiDummy, networkidBics, 'onDialogTimeoutafterSRIRequest', 'sg_11')
        #
        #         # Row 3 -- SRI timeout -- GT 61491500050 -- 1 Insert, 3 Update
        #         GenericTotal(insertSriTimeOut, gtsg2, r2, ccsg, statusDummy, 'failed1', systemDummy, imsiDummy, networkidTATA, 'onDialogTimeoutafterSRIRequest', 'sg_12')
        #         GenericTotal(updateSriTimeOut, gtsg2, r2, ccsg, statusDummy, 'failed2', systemDummy, imsiDummy, networkidibasis, 'onDialogTimeoutafterSRIRequest', 'sg_12')
        #         GenericTotal(updateSriTimeOut, gtsg2, r2, ccsg, statusDummy, 'failed3', systemDummy, imsiDummy, networkidComfone, 'onDialogTimeoutafterSRIRequest', 'sg_12')
        #         GenericTotal(updateSriTimeOut, gtsg2, r2, ccsg, statusDummy, 'failed4', systemDummy, imsiDummy, networkidBics, 'onDialogTimeoutafterSRIRequest', 'sg_12')
        #
        #         # Row 4 -- FWSM failure -- GT 3197015001050 -- 1 Insert, 7 Updates
        #         GenericTotal(insertMtFail, gtsg1, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi1, networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_13')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi1, networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_13')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi1, networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_13')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi1, networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_13')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi1, networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_13')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi1, networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_13')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi1, networkidBics, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_13')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi1, networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_13')
        #
        #
        #         # Row 5 -- FWSM failure -- GT 61491500050 -- 1 Insert, 7 Updates
        #         GenericTotal(insertMtFail, gtsg2, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi1, networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_14')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi1, networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_14')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi1, networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_14')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi1, networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_14')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi1, networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_14')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi1, networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_14')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi1, networkidBics, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_14')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi1, networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_14')
        #
        #
        #         # Row 6 -- FWSM failure -- GT 3197015001050 -- 1 Insert, 7 Updates
        #         GenericTotal(insertMtFail, gtsg1, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi2, networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_15')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi2, networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_15')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi2, networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_15')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi2, networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_15')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi2, networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_15')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi2, networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_15')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi2, networkidBics, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_15')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi2, networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_15')
        #
        #         # Row 7 -- FWSM failure -- GT 61491500050 -- 1 Insert, 7 Updates
        #         GenericTotal(insertMtFail, gtsg2, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi2, networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_16')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi2, networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_16')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi2, networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_16')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi2, networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_16')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi2, networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_16')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi2, networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_16')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi2, networkidBics, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_16')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi2, networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_16')
        #
        #         # Row 8 -- FWSM failure -- GT 3197015001050 -- 1 Insert, 7 Updates
        #         GenericTotal(insertMtFail, gtsg1, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi3, networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_17')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi3, networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_17')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi3, networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_17')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi3, networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_17')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi3, networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_17')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi3, networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_17')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi3, networkidBics, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_17')
        #         GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi3, networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_17')
        #
        #         # Row 9 -- FWSM failure -- GT 61491500050 -- 1 Insert, 7 Updates
        #         GenericTotal(insertMtFail, gtsg2, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi3, networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_18')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi3, networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_18')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi3, networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_18')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi3, networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_18')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi3, networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_18')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi3, networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_18')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi3, networkidBics, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_18')
        #         GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi3, networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_18')
        #
        #
        #
        #
        #
        #
        #         # FaceBook Row 1
        #         GenericTotal(insert, gt6994, r2, ccfb, statusTotal, db_err_field, systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_1')
        #         GenericTotal(updateSuc, gt6994, r2, ccfb, statusSuccess, 'success', systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_1')
        #         GenericTotal(updateFail, gt6994, r2, ccfb, statusFailed, 'failed1', systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_1')
        #
        #         # Row 1 column 2 -- SRI Failure -- Primary smsc-2-eu4 -- GT 3197015001052
        #         GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed2', system6, imsiDummy, networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_1')
        #
        #         # Row 1 column 3 -- FWSM Failure -- Primary smsc-2-eu4 -- GT 3197015001052
        #         GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed3', system6, imsiDummy, networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_1')
        #         GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed4', system6, imsiDummy, networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_1')
        #
        #         # Row 1 column 4 -- SRI Failure -- Failover smsc-2-eu1 -- GT 3197015001052
        #         GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed5', system7, imsiDummy, networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_1')
        #
        #         # Row 1 column 5 -- FWSM Failure -- Failover smsc-2-eu1 -- GT 3197015001052
        #         GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed6', system7, imsiDummy, networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_1')
        #         GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed7', system7, imsiDummy, networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_1')
        #
        #
        #         # FaceBook Row 2
        #         GenericTotal(insert, gt6995, r2, ccfb, statusTotal, db_err_field, systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_2')
        #         GenericTotal(updateSuc, gt6995, r2, ccfb, statusSuccess, 'success', systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_2')
        #         GenericTotal(updateFail, gt6995, r2, ccfb, statusFailed, 'failed1', systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_2')
        #
        #         # Row 2 column 2 -- SRI Failure -- Primary smsc-2-eu1 -- GT 3197015001050
        #         GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed2', system7, imsiDummy, networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_2')
        #
        #         # Row 2 column 3 -- FWSM Failure -- Primary smsc-2-eu1 -- GT 3197015001050
        #         GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed3', system7, imsiDummy, networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_2')
        #         GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed4', system7, imsiDummy, networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_2')
        #
        #         # Row 2 column 4 -- SRI Failure -- Failover smsc-2-eu4 -- GT 3197015001050
        #         GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed5', system6, imsiDummy, networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_2')
        #
        #         # Row 2 column 5 -- FWSM Failure -- Failover smsc-2-eu1 -- GT 3197015001050
        #         GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed6', system6, imsiDummy, networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_2')
        #         GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed7', system6, imsiDummy, networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_2')
        #
        #         # FaceBook Row 3
        #         GenericTotal(insert, gt6908, r2, ccfb, statusTotal, db_err_field, systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_3')
        #         GenericTotal(updateSuc, gt6908, r2, ccfb, statusSuccess, 'success', systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_3')
        #         GenericTotal(updateFail, gt6908, r2, ccfb, statusFailed, 'failed1', systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_3')
        #
        #         # Row 3 column 2 -- SRI Failure -- All SMSCs -- GT 3197015001051
        #         GenericTotal(updateMtFailure, gt6908, r2, ccfb, statusDummy, 'failed2', system5, imsiDummy, networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_3')
        #
        #         # Row 3 column 3 -- FWSM Failure -- All SMSCs -- GT 3197015001051
        #         GenericTotal(updateMtFailure, gt6908, r2, ccfb, statusDummy, 'failed3', system5, imsiDummy, networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_3')
        #         GenericTotal(updateMtFailure, gt6908, r2, ccfb, statusDummy, 'failed4', system5, imsiDummy, networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_3')
        #
        #         # FaceBook Row 4
        #         GenericTotal(insert, gt6909, r2, ccfb, statusTotal, db_err_field, systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_4')
        #         GenericTotal(updateSuc, gt6909, r2, ccfb, statusSuccess, 'success', systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_4')
        #         GenericTotal(updateFail, gt6909, r2, ccfb, statusFailed, 'failed1', systemDummy, imsiDummy, networkidDummy, error_msg, 'fb_4')
        #
        #         # Row 4 column 2 -- SRI Failure -- All SMSCs -- GT 3197015001053
        #         GenericTotal(updateMtFailure, gt6909, r2, ccfb, statusDummy, 'failed2', system5, imsiDummy, networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_4')
        #
        #         # Row 4 column 3 -- FWSM Failure -- All SMSCs -- GT 3197015001053
        #         GenericTotal(updateMtFailure, gt6909, r2, ccfb, statusDummy, 'failed3', system5, imsiDummy, networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_4')
        #         GenericTotal(updateMtFailure, gt6909, r2, ccfb, statusDummy, 'failed4', system5, imsiDummy, networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_4')
        #
        #
        #
        #
        #     cur.close()


        else:
            my_new_date = request.POST.get("date")
            my_new_NetworkID = request.POST.get("NetworkID")
            my_new_smsc = request.POST.get("smsc")
            if my_new_date == '0':
                today = (date.today() - timedelta(days=0)).strftime('%m-%d')
                p = Popen(["ssh","{}".format(my_new_smsc),"python","/home/kennyC/sms/smsc_script_v4.py","-s","{}".format(my_new_date)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                output, errors = p.communicate()

                try:

                    list = []
                    st = " ".join(output.split('\n'))
                    st = st.split(' ')

                    it = iter(st) #https://stackoverflow.com/questions/16789776/iterating-over-two-values-of-a-list-at-a-time-in-python
                    for a, b, c, d, e, f, g, h, i, j in zip(*[iter(it)]*10):
                        print (a, b, c, d, e, f, g, h, i, j)
                        p = CdrProcess(
                        msisdn="{}".format(a),
                        status="{}".format(b),
                        networkid="{}".format(c),
                        date="{}".format(d),
                        time="{}".format(e),
                        gt="{}".format(f),
                        system="{}".format(g),
                        msc="{}".format(h),
                        imsi="{}".format(i),
                        error_msg="{}".format(j),
                        )
                        p.save()
                except:
                    pass

            elif my_new_date == 'examplefile':
                # print ("examplefile")
                p = Popen(["ssh","{}".format(my_new_smsc),"python","/home/kennyC/sms/smsc_script_v4.py","-s","{}".format(my_new_date)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                output, errors = p.communicate()

                try:

                    list = []
                    st = " ".join(output.split('\n'))
                    st = st.split(' ')

                    it = iter(st) #https://stackoverflow.com/questions/16789776/iterating-over-two-values-of-a-list-at-a-time-in-python
                    for a, b, c, d, e, f, g, h, i, j in zip(*[iter(it)]*10):
                        print (a, b, c, d, e, f, g, h, i, j)
                        p = CdrProcess(
                        msisdn="{}".format(a),
                        status="{}".format(b),
                        networkid="{}".format(c),
                        date="{}".format(d),
                        time="{}".format(e),
                        gt="{}".format(f),
                        system="{}".format(g),
                        msc="{}".format(h),
                        imsi="{}".format(i),
                        error_msg="{}".format(j),
                        )
                        p.save()
                        # print (p)
                except:
                    pass

            elif my_new_date == '-1':
                p = Popen(["ssh","{}".format(my_new_smsc),"python","/home/kennyC/sms/smsc_script_v4.py","-s","{}".format(my_new_date)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                output, errors = p.communicate()

                try:

                    list = []
                    st = " ".join(output.split('\n'))
                    st = st.split(' ')

                    it = iter(st) #https://stackoverflow.com/questions/16789776/iterating-over-two-values-of-a-list-at-a-time-in-python
                    for a, b, c, d, e, f, g, h, i, j in zip(*[iter(it)]*10):
                        print (a, b, c, d, e, f, g, h, i, j)
                        p = CdrProcess(
                        msisdn="{}".format(a),
                        status="{}".format(b),
                        networkid="{}".format(c),
                        date="{}".format(d),
                        time="{}".format(e),
                        gt="{}".format(f),
                        system="{}".format(g),
                        msc="{}".format(h),
                        imsi="{}".format(i),
                        error_msg="{}".format(j),
                        )
                        p.save()
                        # print (p)
                except:
                    pass
            elif my_new_date == '-2':
                p = Popen(["ssh","{}".format(my_new_smsc),"python","/home/kennyC/sms/smsc_script_v4.py","-s","{}".format(my_new_date)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                output, errors = p.communicate()

                try:

                    list = []
                    st = " ".join(output.split('\n'))
                    st = st.split(' ')

                    it = iter(st) #https://stackoverflow.com/questions/16789776/iterating-over-two-values-of-a-list-at-a-time-in-python
                    for a, b, c, d, e, f, g, h, i, j in zip(*[iter(it)]*10):
                        print (a, b, c, d, e, f, g, h, i, j)
                        p = CdrProcess(
                        msisdn="{}".format(a),
                        status="{}".format(b),
                        networkid="{}".format(c),
                        date="{}".format(d),
                        time="{}".format(e),
                        gt="{}".format(f),
                        system="{}".format(g),
                        msc="{}".format(h),
                        imsi="{}".format(i),
                        error_msg="{}".format(j),
                        )
                        p.save()


                    con = sqlite3.connect('db.sqlite3')    # From here read from crm_cdrprocess and inseert into crm_cdrtable
                    cur = con.cursor()

                    # DB_mode
                    insert = 'insert'
                    update = 'update'
                    updateMtFailed = 'updateMtFailed'
                    updateMtFwFailed = 'updateMtFwFailed'
                    updateMtFailure = 'updateMtFailure'
                    insertSriFB = 'insertSriFB'
                    insertMtFB = 'insertMtFB'
                    updateMtFB = 'updateMtFB'
                    insertmt = 'insertmt'
                    updateSuc = 'updateSuc'
                    updateFail = 'updateFail'
                    insertsgsrito = 'insertsgsrito'
                    insertSriTimeOut = 'insertSriTimeOut'
                    insertMtFail = 'insertMtFail'
                    updateMtFail = 'updateMtFail'
                    updateSriTimeOut = 'updateSriTimeOut'
                    insertMtTimeOut = 'insertMtTimeOut'
                    updateMtSysFail = 'updateMtSysFail'

                    insert1gt = 'insert1gt'
                    insert2gt = 'insert2gt'

                    ccsg = '65'
                    ccms = '91'
                    ccfb = '91'

                    gt_sg = '3197015001050,', '61491500050,'
                    gt_sg1 = '3197015001050,'
                    gt_sg2 = '61491500050,'

                    gt_6995 = '3197015001050,'
                    gt_6994 = '3197015001052,'
                    gt_6908 = '3197015001051,'
                    gt_6909 = '3197015001053,'
                    gt_dummy = 'dummy'

                    smsc = 'smsc-1-eu1,', 'smsc-2-eu1,', 'smsc-1-eu4,', 'smsc-2-eu4,'
                    smsc1 = 'smsc-1-eu1,'
                    smsc2 = 'smsc-2-eu1,'
                    smsc3 = 'smsc-1-eu4,'
                    smsc4 = 'smsc-2-eu4,'
                    smscDummy = 'smscDummy'

                    system1 = 'smsc-1-eu1,'
                    system2 = 'smsc-2-eu1,'
                    system3 = 'smsc-1-eu4,'
                    system4 = 'smsc-2-eu4,'
                    system5 = 'smsc-1-eu1,', 'smsc-2-eu1,', 'smsc-1-eu4,', 'smsc-2-eu4,'
                    system6 = 'smsc-2-eu4,', 'smsc-2-eu4,', 'smsc-2-eu4,', 'smsc-2-eu4,'
                    system7 = 'smsc-2-eu1,', 'smsc-2-eu1,', 'smsc-2-eu1,', 'smsc-2-eu1,'

                    systemDummy = 'dummy'

                    success = 'success,'
                    partial = 'partial,'
                    failed = 'failed,'
                    temp_failed = 'temp_failed,'

                    statusTotal = 'failed,', 'success,', 'temp_failed,'
                    statusSuccess = 'success,', 'dummy', 'dummy'  # 2x dummy
                    statusFailed = 'failed,', 'temp_failed,', 'dummy'  # 1x dummy
                    statusDummy = 'dummy', 'dummy', 'dummy'  # 3x dummy

                    imsi1 = '52501'
                    imsi2 = '52503'
                    imsi3 = '52505'
                    imsi7 = '4058'
                    imsiDummy = 'dummy'

                    tata = 'tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,'
                    ibasis = 'ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,', 'ibasisc01,'
                    comfone = 'comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,'
                    bics = 'bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,', 'bicsc01,'

                    networkidTATA = 'tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,'
                    networkidibasis = 'ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,', 'ibasisc01,'
                    networkidComfone = 'comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,'
                    networkidBics = 'bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,', 'bicsc01,'
                    networkidDummy = 'dummy'

                    gtsg = '3197015001050,', '61491500050,'
                    gtsg1 = '3197015001050,', '3197015001050,'
                    gtsg2 = '61491500050,', '61491500050,'

                    gt6995 = '3197015001050,', '3197015001050,'
                    gt6994 = '3197015001052,', '3197015001052,'
                    gt6908 = '3197015001051,', '3197015001051,'
                    gt6909 = '3197015001053,', '3197015001053,'

                    error_msg = 'error_msg'

                    db_err_field = 'db_err_field'

                    s1 = list2hourv2()
                    print("effe testen {}".format(s1))

                    r1 = list2hourv2()
                    for x in r1:
                        # Row 1
                        r2 = ("{}:{}".format(x[0], x[1]))
                        print(r2)

                        # Row 1 column 1 for Generic total, success, failed v3
                        GenericTotal(insert, gtsg, r2, ccsg, statusTotal, db_err_field, systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'sg_10')
                        GenericTotal(updateSuc, gtsg, r2, ccsg, statusSuccess, 'success', systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'sg_10')
                        GenericTotal(updateFail, gtsg, r2, ccsg, statusFailed, 'failed1', systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'sg_10')

                        # Row 1 column 2 All MNO SRI timeouts
                        GenericTotal(updateMtFailed, gtsg, r2, ccsg, statusDummy, 'failed2', systemDummy, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterSRIRequest', 'sg_10')

                        # Row 1 column 3 fwsm timeout and SystemFailed for SingTel
                        GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi1,
                                     networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_10')
                        GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi1,
                                     networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_10')

                        # Row 1 column 3 fwsm timeout and SystemFailed for M1
                        GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi2,
                                     networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_10')
                        GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi2,
                                     networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_10')

                        # Row 1 column 3 fwsm timeout and SystemFailed for StarHub
                        GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi3,
                                     networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_10')
                        GenericTotal(updateMtFwFailed, gtsg, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi3,
                                     networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_10')

                        # Row 2 -- SRI timeout -- GT 3197015001050 -- 1 Insert, 3 Update
                        GenericTotal(insertSriTimeOut, gtsg1, r2, ccsg, statusDummy, 'failed1', systemDummy, imsiDummy,
                                     networkidTATA, 'onDialogTimeoutafterSRIRequest', 'sg_11')
                        GenericTotal(updateSriTimeOut, gtsg1, r2, ccsg, statusDummy, 'failed2', systemDummy, imsiDummy,
                                     networkidibasis, 'onDialogTimeoutafterSRIRequest', 'sg_11')
                        GenericTotal(updateSriTimeOut, gtsg1, r2, ccsg, statusDummy, 'failed3', systemDummy, imsiDummy,
                                     networkidComfone, 'onDialogTimeoutafterSRIRequest', 'sg_11')
                        GenericTotal(updateSriTimeOut, gtsg1, r2, ccsg, statusDummy, 'failed4', systemDummy, imsiDummy,
                                     networkidBics, 'onDialogTimeoutafterSRIRequest', 'sg_11')

                        # Row 3 -- SRI timeout -- GT 61491500050 -- 1 Insert, 3 Update
                        GenericTotal(insertSriTimeOut, gtsg2, r2, ccsg, statusDummy, 'failed1', systemDummy, imsiDummy,
                                     networkidTATA, 'onDialogTimeoutafterSRIRequest', 'sg_12')
                        GenericTotal(updateSriTimeOut, gtsg2, r2, ccsg, statusDummy, 'failed2', systemDummy, imsiDummy,
                                     networkidibasis, 'onDialogTimeoutafterSRIRequest', 'sg_12')
                        GenericTotal(updateSriTimeOut, gtsg2, r2, ccsg, statusDummy, 'failed3', systemDummy, imsiDummy,
                                     networkidComfone, 'onDialogTimeoutafterSRIRequest', 'sg_12')
                        GenericTotal(updateSriTimeOut, gtsg2, r2, ccsg, statusDummy, 'failed4', systemDummy, imsiDummy,
                                     networkidBics, 'onDialogTimeoutafterSRIRequest', 'sg_12')

                        # Row 4 -- FWSM failure -- GT 3197015001050 -- 1 Insert, 7 Updates
                        GenericTotal(insertMtFail, gtsg1, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi1,
                                     networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_13')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi1,
                                     networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_13')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi1,
                                     networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_13')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi1,
                                     networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_13')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi1,
                                     networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_13')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi1,
                                     networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_13')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi1,
                                     networkidBics, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_13')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi1,
                                     networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_13')

                        # Row 5 -- FWSM failure -- GT 61491500050 -- 1 Insert, 7 Updates
                        GenericTotal(insertMtFail, gtsg2, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi1,
                                     networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_14')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi1,
                                     networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_14')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi1,
                                     networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_14')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi1,
                                     networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_14')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi1,
                                     networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_14')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi1,
                                     networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_14')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi1,
                                     networkidBics, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_14')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi1,
                                     networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_14')

                        # Row 6 -- FWSM failure -- GT 3197015001050 -- 1 Insert, 7 Updates
                        GenericTotal(insertMtFail, gtsg1, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi2,
                                     networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_15')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi2,
                                     networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_15')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi2,
                                     networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_15')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi2,
                                     networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_15')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi2,
                                     networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_15')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi2,
                                     networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_15')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi2,
                                     networkidBics, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_15')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi2,
                                     networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_15')

                        # Row 7 -- FWSM failure -- GT 61491500050 -- 1 Insert, 7 Updates
                        GenericTotal(insertMtFail, gtsg2, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi2,
                                     networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_16')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi2,
                                     networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_16')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi2,
                                     networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_16')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi2,
                                     networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_16')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi2,
                                     networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_16')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi2,
                                     networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_16')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi2,
                                     networkidBics, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_16')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi2,
                                     networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_16')

                        # Row 8 -- FWSM failure -- GT 3197015001050 -- 1 Insert, 7 Updates
                        GenericTotal(insertMtFail, gtsg1, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi3,
                                     networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_17')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi3,
                                     networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_17')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi3,
                                     networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_17')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi3,
                                     networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_17')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi3,
                                     networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_17')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi3,
                                     networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_17')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi3,
                                     networkidBics, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_17')
                        GenericTotal(updateMtFail, gtsg1, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi3,
                                     networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_17')

                        # Row 9 -- FWSM failure -- GT 61491500050 -- 1 Insert, 7 Updates
                        GenericTotal(insertMtFail, gtsg2, r2, ccsg, statusDummy, 'failed1', systemDummy, imsi3,
                                     networkidTATA, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_18')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed2', systemDummy, imsi3,
                                     networkidTATA, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_18')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed3', systemDummy, imsi3,
                                     networkidibasis, 'onDialogTimeoutafterMtForwardSMRequest', 'sg_18')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed4', systemDummy, imsi3,
                                     networkidibasis, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_18')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed5', systemDummy, imsi3,
                                     networkidComfone, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_18')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed6', systemDummy, imsi3,
                                     networkidComfone, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_18')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed7', systemDummy, imsi3,
                                     networkidBics, 'onDialogTimeoutafterMtForwardSMRequest:', 'sg_18')
                        GenericTotal(updateMtFail, gtsg2, r2, ccsg, statusDummy, 'failed8', systemDummy, imsi3,
                                     networkidBics, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'sg_18')

                        # FaceBook Row 1
                        GenericTotal(insert, gt6994, r2, ccfb, statusTotal, db_err_field, systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_1')
                        GenericTotal(updateSuc, gt6994, r2, ccfb, statusSuccess, 'success', systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_1')
                        GenericTotal(updateFail, gt6994, r2, ccfb, statusFailed, 'failed1', systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_1')

                        # Row 1 column 2 -- SRI Failure -- Primary smsc-2-eu4 -- GT 3197015001052
                        GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed2', system6, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_1')

                        # Row 1 column 3 -- FWSM Failure -- Primary smsc-2-eu4 -- GT 3197015001052
                        GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed3', system6, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_1')
                        GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed4', system6, imsiDummy,
                                     networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_1')

                        # Row 1 column 4 -- SRI Failure -- Failover smsc-2-eu1 -- GT 3197015001052
                        GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed5', system7, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_1')

                        # Row 1 column 5 -- FWSM Failure -- Failover smsc-2-eu1 -- GT 3197015001052
                        GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed6', system7, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_1')
                        GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed7', system7, imsiDummy,
                                     networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_1')

                        # FaceBook Row 2
                        GenericTotal(insert, gt6995, r2, ccfb, statusTotal, db_err_field, systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_2')
                        GenericTotal(updateSuc, gt6995, r2, ccfb, statusSuccess, 'success', systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_2')
                        GenericTotal(updateFail, gt6995, r2, ccfb, statusFailed, 'failed1', systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_2')

                        # Row 2 column 2 -- SRI Failure -- Primary smsc-2-eu1 -- GT 3197015001050
                        GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed2', system7, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_2')

                        # Row 2 column 3 -- FWSM Failure -- Primary smsc-2-eu1 -- GT 3197015001050
                        GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed3', system7, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_2')
                        GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed4', system7, imsiDummy,
                                     networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_2')

                        # Row 2 column 4 -- SRI Failure -- Failover smsc-2-eu4 -- GT 3197015001050
                        GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed5', system6, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_2')

                        # Row 2 column 5 -- FWSM Failure -- Failover smsc-2-eu1 -- GT 3197015001050
                        GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed6', system6, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_2')
                        GenericTotal(updateMtFailure, gt6995, r2, ccfb, statusDummy, 'failed7', system6, imsiDummy,
                                     networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_2')

                        # FaceBook Row 3
                        GenericTotal(insert, gt6908, r2, ccfb, statusTotal, db_err_field, systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_3')
                        GenericTotal(updateSuc, gt6908, r2, ccfb, statusSuccess, 'success', systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_3')
                        GenericTotal(updateFail, gt6908, r2, ccfb, statusFailed, 'failed1', systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_3')

                        # Row 3 column 2 -- SRI Failure -- All SMSCs -- GT 3197015001051
                        GenericTotal(updateMtFailure, gt6908, r2, ccfb, statusDummy, 'failed2', system5, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_3')

                        # Row 3 column 3 -- FWSM Failure -- All SMSCs -- GT 3197015001051
                        GenericTotal(updateMtFailure, gt6908, r2, ccfb, statusDummy, 'failed3', system5, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_3')
                        GenericTotal(updateMtFailure, gt6908, r2, ccfb, statusDummy, 'failed4', system5, imsiDummy,
                                     networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_3')

                        # FaceBook Row 4
                        GenericTotal(insert, gt6909, r2, ccfb, statusTotal, db_err_field, systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_4')
                        GenericTotal(updateSuc, gt6909, r2, ccfb, statusSuccess, 'success', systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_4')
                        GenericTotal(updateFail, gt6909, r2, ccfb, statusFailed, 'failed1', systemDummy, imsiDummy,
                                     networkidDummy, error_msg, 'fb_4')

                        # Row 4 column 2 -- SRI Failure -- All SMSCs -- GT 3197015001053
                        GenericTotal(updateMtFailure, gt6909, r2, ccfb, statusDummy, 'failed2', system5, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterSRIRequest', 'fb_4')

                        # Row 4 column 3 -- FWSM Failure -- All SMSCs -- GT 3197015001053
                        GenericTotal(updateMtFailure, gt6909, r2, ccfb, statusDummy, 'failed3', system5, imsiDummy,
                                     networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_4')
                        GenericTotal(updateMtFailure, gt6909, r2, ccfb, statusDummy, 'failed4', system5, imsiDummy,
                                     networkidDummy, 'ErrorsmDeliveryFailureafterMtForwardSMRequest:', 'fb_4')

                    cur.close()
                except:
                    pass
            else:
                pass

    count_total_smsc_2_eu4 = CdrProcess.objects.all().count()

    context={
        'count_total_smsc_2_eu4' : count_total_smsc_2_eu4
        }
    return render(request, 'crm/smsc.html', context)




def cdr_detail_view(request):
    min0 = 0
    min1 = 1
    min2 = 2
    min3 = 3
    min4 = 4
    min5 = 5

    min = [0, 1, 2, 3, 4, 5]


    return render(request, "crm/dashboard.html", {})


def fb(request):
    if request.method == 'POST':
        if request.POST.get("insertFBdata") == 'insertFBdata':
            insertFBdata = request.POST.get("insertFBdata")
            con = sqlite3.connect('db.sqlite3')
            cur = con.cursor()
            ccms = '91'
            r1 = list2hourv2()
            for x in r1:
                r2 = ("{}:{}".format(x[0], x[1]))
                con.commit()
            cur.close()


    cdrTable_fb_1 = cdrTable.objects.filter(row_id='fb_1').order_by('time')
    cdrTable_fb_2 = cdrTable.objects.filter(row_id='fb_2').order_by('time')
    cdrTable_fb_3 = cdrTable.objects.filter(row_id='fb_3').order_by('time')
    cdrTable_fb_4 = cdrTable.objects.filter(row_id='fb_4').order_by('time')

    context = {
        'cdrTable_fb_1': cdrTable_fb_1,
        'cdrTable_fb_2': cdrTable_fb_2,
        'cdrTable_fb_3': cdrTable_fb_3,
        'cdrTable_fb_4': cdrTable_fb_4,
    }

    return render(request, 'crm/fb.html', context )




def newSGv3(request):

    cdrTable_sg_10 = cdrTable.objects.filter(row_id='sg_10').order_by('time')
    cdrTable_sg_11 = cdrTable.objects.filter(row_id='sg_11').order_by('time')
    cdrTable_sg_12 = cdrTable.objects.filter(row_id='sg_12').order_by('time')
    cdrTable_sg_13 = cdrTable.objects.filter(row_id='sg_13').order_by('time')
    cdrTable_sg_14 = cdrTable.objects.filter(row_id='sg_14').order_by('time')
    cdrTable_sg_15 = cdrTable.objects.filter(row_id='sg_15').order_by('time')
    cdrTable_sg_16 = cdrTable.objects.filter(row_id='sg_16').order_by('time')
    cdrTable_sg_17 = cdrTable.objects.filter(row_id='sg_17').order_by('time')
    cdrTable_sg_18 = cdrTable.objects.filter(row_id='sg_18').order_by('time')


    context = {
        'cdrTable_sg_10': cdrTable_sg_10,
        'cdrTable_sg_11': cdrTable_sg_11,
        'cdrTable_sg_12': cdrTable_sg_12,
        'cdrTable_sg_13': cdrTable_sg_13,
        'cdrTable_sg_14': cdrTable_sg_14,
        'cdrTable_sg_15': cdrTable_sg_15,
        'cdrTable_sg_16': cdrTable_sg_16,
        'cdrTable_sg_17': cdrTable_sg_17,
        'cdrTable_sg_18': cdrTable_sg_18,

    }
    return render(request, 'crm/newSGv3.html', context)


def list2hourv2():
    min = [0, 1, 2, 3, 4, 5]
    hourlist = []
    dt = datetime.today() - timedelta(hours=1, minutes=0)  # Get time and extract 1 hour of it
    t1 = dt.strftime('%H')  # Get time and only get the hour
    get_date = datetime.now().strftime('%m-%d')  # Get month and day

    dt2 = datetime.today() - timedelta(hours=0, minutes=0)  # Get current time
    t2 = dt2.strftime('%H')  # Get time and only get the hour

    hourlist.append(t1)
    hourlist.append(t2)
    prod = product(hourlist, min)

    return (list(prod))


def GenericTotal(mode, gt, time, msisdn, status, db_err_field, system, imsi, networkid, error_msg, tableid):

    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    if 'insert' == mode:
        cur.execute("SELECT count(*) FROM crm_cdrprocess where gt IN ('{}', '{}')  and time like '{}%' and msisdn like '{}%' and status IN ('{}', '{}', '{}')".format(gt[0], gt[1], time, msisdn, status[0], status[1], status[2]))
        result1 = cur.fetchone()
        cur.execute("insert into crm_cdrTable (time, total, success, failed1, failed2, failed3, failed4, failed5, failed6, failed7, failed8, row_id) VALUES ('{}', '{}', '', '', '', '', '', '', '', '', '', '{}');".format(time, result1[0], tableid)) # insert total
        con.commit()
    elif 'updateSuc' == mode:
        cur.execute("SELECT count(*) FROM crm_cdrprocess where gt IN ('{}', '{}')  and time like '{}%' and msisdn like '{}%' and status IN ('{}', '{}', '{}')".format(gt[0], gt[1], time, msisdn, status[0], status[1], status[2]))
        result1 = cur.fetchone()
        cur.execute("UPDATE crm_cdrTable SET '{}' = '{}' WHERE time like '{}%' and row_id = '{}';".format(db_err_field, result1[0], time, tableid))
        con.commit()
    elif 'updateFail' == mode:
        cur.execute("SELECT count(*) FROM crm_cdrprocess where gt IN ('{}', '{}')  and time like '{}%' and msisdn like '{}%' and status IN ('{}', '{}', '{}')".format(gt[0], gt[1], time, msisdn, status[0], status[1], status[2]))
        result1 = cur.fetchone()
        cur.execute("UPDATE crm_cdrTable SET '{}' = '{}' WHERE time like '{}%' and row_id = '{}';".format(db_err_field, result1[0], time, tableid))
        con.commit()
    elif 'updateMtFailed' == mode:
        cur.execute("SELECT count(*) FROM crm_cdrprocess where gt IN ('{}', '{}')  and time like '{}%' and msisdn like '{}%' and error_msg = '{}'".format(gt[0], gt[1], time, msisdn, error_msg))
        result1 = cur.fetchone()
        cur.execute("UPDATE crm_cdrTable SET '{}' = '{}' WHERE time like '{}%' and row_id = '{}';".format(db_err_field, result1[0], time, tableid))
        con.commit()
    elif 'updateMtFwFailed' == mode:
        cur.execute("SELECT count(*) FROM crm_cdrprocess where gt IN ('{}', '{}')  and time like '{}%' and msisdn like '{}%' and error_msg = '{}' and imsi like '{}%'".format(gt[0], gt[1], time, msisdn, error_msg, imsi))
        result1 = cur.fetchone()
        cur.execute("UPDATE crm_cdrTable SET '{}' = '{}' WHERE time like '{}%' and row_id = '{}';".format(db_err_field, result1[0], time, tableid))
        con.commit()
    elif 'insertSriTimeOut' == mode:
        cur.execute("SELECT count(*) FROM crm_cdrprocess where gt IN ('{}', '{}')  and time like '{}%' and msisdn like '{}%' and networkid IN ('{}', '{}', '{}', '{}', '{}', '{}', '{}') and error_msg = '{}'".format(gt[0], gt[1], time, msisdn, networkid[0], networkid[1], networkid[2], networkid[3], networkid[4], networkid[5], networkid[6], error_msg))
        result1 = cur.fetchone()
        cur.execute("insert into crm_cdrTable (time, total, success, failed1, failed2, failed3, failed4, failed5, failed6, failed7, failed8, row_id) VALUES ('{}', '', '', '{}', '', '', '', '', '', '', '', '{}');".format(time, result1[0], tableid))
        con.commit()
    elif 'updateSriTimeOut' == mode:
        cur.execute("SELECT count(*) FROM crm_cdrprocess where gt IN ('{}', '{}')  and time like '{}%' and msisdn like '{}%' and networkid IN ('{}', '{}', '{}', '{}', '{}', '{}', '{}') and error_msg = '{}'".format(gt[0], gt[1], time, msisdn, networkid[0], networkid[1], networkid[2], networkid[3], networkid[4], networkid[5], networkid[6], error_msg))
        result1 = cur.fetchone()
        cur.execute("UPDATE crm_cdrTable SET '{}' = '{}' WHERE time like '{}%' and row_id = '{}';".format(db_err_field, result1[0], time, tableid))
        con.commit()
    elif 'insertMtFail' == mode:
        cur.execute("SELECT count(*) FROM crm_cdrprocess where gt IN ('{}', '{}')  and time like '{}%' and msisdn like '{}%' and imsi like '{}%' and networkid IN ('{}', '{}', '{}', '{}', '{}', '{}', '{}') and error_msg = '{}' ".format(gt[0], gt[1], time, msisdn, imsi, networkid[0], networkid[1], networkid[2], networkid[3], networkid[4], networkid[5], networkid[6], error_msg))
        result1 = cur.fetchone()
        cur.execute("insert into crm_cdrTable (time, total, success, failed1, failed2, failed3, failed4, failed5, failed6, failed7, failed8, row_id) VALUES ('{}', '', '', '{}', '', '', '', '', '', '', '', '{}');".format(time, result1[0], tableid))
        con.commit()
    elif 'updateMtFail' == mode:
        cur.execute("SELECT count(*) FROM crm_cdrprocess where gt IN ('{}', '{}')  and time like '{}%' and msisdn like '{}%' and imsi like '{}%' and networkid IN ('{}', '{}', '{}', '{}', '{}', '{}', '{}') and error_msg = '{}' ".format(gt[0], gt[1], time, msisdn, imsi, networkid[0], networkid[1], networkid[2], networkid[3], networkid[4], networkid[5], networkid[6], error_msg))
        result1 = cur.fetchone()
        cur.execute("UPDATE crm_cdrTable SET '{}' = '{}' WHERE time like '{}%' and row_id = '{}';".format(db_err_field, result1[0], time, tableid))
        con.commit()
    elif 'updateMtFailure' == mode:
        # GenericTotal(updateMtFailure, gt6994, r2, ccfb, statusDummy, 'failed3', system6, networkidDummy, 'onDialogTimeoutafterMtForwardSMRequest', 'fb_1')
        cur.execute("SELECT count(*) FROM crm_cdrprocess where gt IN ('{}', '{}')  and time like '{}%' and msisdn like '{}%' and system IN ('{}', '{}', '{}', '{}') and error_msg = '{}'".format(gt[0], gt[1], time, msisdn, system[0], system[1], system[2], system[3], error_msg))
        result1 = cur.fetchone()
        cur.execute("UPDATE crm_cdrTable SET '{}' = '{}' WHERE time like '{}%' and row_id = '{}';".format(db_err_field, result1[0], time, tableid))
        con.commit()
    else:
        print ("not found")


