from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import CdrProcess, EsmeDlr
import logging
import subprocess
from datetime import date, timedelta
from subprocess import PIPE, Popen
from django.db.models import Q

logger = logging.getLogger(__name__)





def home(request):
    success_min0_smsc_2_eu4 = CdrProcess.objects.filter(status__exact="success").count()

    context = {
        'success_min0_smsc_2_eu4' : success_min0_smsc_2_eu4,
    }
    return render(request, "crm/dashboard.html", context)


def reset(request):
    print(request.POST)
    if request.method == 'POST':
        reset = request.POST.get("reset")
        print (reset)
        
        CdrProcess.objects.all().delete()   # Delete records from DB
        q = CdrProcess(time="00:00:00.000,", date='1999-99-99', msisdn='9999') # Insert 1 default record in DB and save it
        q.save()

    count_total_smsc_2_eu4  = CdrProcess.objects.all().count()

    context = {
        'count_total_smsc_2_eu4' : count_total_smsc_2_eu4,
    }
    return render(request, "crm/reset.html", context)

def esme_dlr_reset(request):
    print(request.POST)
    if request.method == 'POST':
        reset = request.POST.get("reset")
        print (reset)
        EsmeDlr.objects.all().delete()   # Delete records from DB
  

    count_total_smsc_2_eu4  = CdrProcess.objects.all().count()

    context = {
        'count_total_smsc_2_eu4' : count_total_smsc_2_eu4,
    }
    return render(request, "crm/esme_dlr_reset.html", context)





def customer(request):
    return render(request, 'crm/customer.html')

def smsc(request):
    return render(request, 'crm/smsc.html')



def esme_dlr(request):
    print(request.POST)
    if request.method == 'POST':
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
        my_new_date = request.POST.get("date")
        my_new_NetworkID = request.POST.get("NetworkID")
        my_new_smsc = request.POST.get("smsc")
        if my_new_date == '0':
            today = (date.today() - timedelta(days=0)).strftime('%m-%d')
            p = Popen(["ssh","{}".format(my_new_smsc),"python","/home/kennyC/sms/smsc_script_v3.py","-s","{}".format(my_new_date),"{}".format(my_new_NetworkID)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

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
            p = Popen(["ssh","{}".format(my_new_smsc),"python","/home/kennyC/sms/smsc_script_v3.py","-s","{}".format(my_new_date),"{}".format(my_new_NetworkID)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

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
            p = Popen(["ssh","{}".format(my_new_smsc),"python","/home/kennyC/sms/smsc_script_v3.py","-s","{}".format(my_new_date),"{}".format(my_new_NetworkID)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

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
    
    get_time = CdrProcess.objects.all().order_by("-id")[:1].values_list().get() #(1887655, '2021-02-23', '14:23:22.367,', '6592723109,', 'success,', '3197015001050,', '1003,', 'smsc-2-eu4')
    get_time_join = (''.join(get_time[2])) #Get third element and make it to string 
    final_time = ("{}".format(get_time_join[:5])) # Get 5 char from string = mm:ss
    get_hour = ("{}".format(get_time_join[:3])) # Get 3 char from string = mm:
  


    total_min0_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min0)).exclude(status__exact="partial,").count()
    total_min1_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min1)).exclude(status__exact="partial,").count()
    total_min2_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min2)).exclude(status__exact="partial,").count()
    total_min3_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min3)).exclude(status__exact="partial,").count()
    total_min4_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min4)).exclude(status__exact="partial,").count()
    total_min5_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min5)).exclude(status__exact="partial,").count()



    success_min0_smsc_2_eu4 = CdrProcess.objects.filter(status__exact="success,", msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min0)).count()
    success_min1_smsc_2_eu4 = CdrProcess.objects.filter(status__exact="success,", msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min1)).count()
    success_min2_smsc_2_eu4 = CdrProcess.objects.filter(status__exact="success,", msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min2)).count()
    success_min3_smsc_2_eu4 = CdrProcess.objects.filter(status__exact="success,", msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min3)).count()
    success_min4_smsc_2_eu4 = CdrProcess.objects.filter(status__exact="success,", msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min4)).count()
    success_min5_smsc_2_eu4 = CdrProcess.objects.filter(status__exact="success,", msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min5)).count()




    failed_min0_smsc_2_eu4 = CdrProcess.objects.filter(Q(status__exact="failed,") |Q(status__exact="temp_failed,"), msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min0)).count()
    failed_min1_smsc_2_eu4 = CdrProcess.objects.filter(Q(status__exact="failed,") |Q(status__exact="temp_failed,"), msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min1)).count()
    failed_min2_smsc_2_eu4 = CdrProcess.objects.filter(Q(status__exact="failed,") |Q(status__exact="temp_failed,"), msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min2)).count()
    failed_min3_smsc_2_eu4 = CdrProcess.objects.filter(Q(status__exact="failed,") |Q(status__exact="temp_failed,"), msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min3)).count()
    failed_min4_smsc_2_eu4 = CdrProcess.objects.filter(Q(status__exact="failed,") |Q(status__exact="temp_failed,"), msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min4)).count()
    failed_min5_smsc_2_eu4 = CdrProcess.objects.filter(Q(status__exact="failed,") |Q(status__exact="temp_failed,"), msisdn__startswith="65", system__exact="smsc-2-eu4,", time__startswith="{}{}".format(get_hour, min5)).count()



    count_success_smsc_2_eu4 = CdrProcess.objects.filter(status__exact="success,", msisdn__startswith="65", system__exact="smsc-2-eu4,").count()
    count_temp_failed_smsc_2_eu4 = CdrProcess.objects.filter(status__exact="temp_failed,", msisdn__startswith="65", system__exact="smsc-2-eu4,").count()
    count_failed_smsc_2_eu4 =  CdrProcess.objects.filter(status__exact="failed,", msisdn__startswith="65", system__exact="smsc-2-eu4,").count()
    count_total_smsc_2_eu4  = CdrProcess.objects.all().count()


    # SRI part

    sri_min0_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    sri_min1_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    sri_min2_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    sri_min3_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    sri_min4_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    sri_min5_smsc_2_eu4 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", time__startswith="{}{}".format(get_hour, min5)).count()


    # MTFS failure for 52501 Singtel

    mtfs_min0_smsc_2_eu4 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_min1_smsc_2_eu4 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_min2_smsc_2_eu4 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_min3_smsc_2_eu4 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_min4_smsc_2_eu4 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_min5_smsc_2_eu4 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()

    


    # MTFS failure for 52505 Singtel

    mtfs_min0_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_min1_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_min2_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_min3_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_min4_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_min5_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()



    # MTFS failure for 52503 M1

    mtfs_52503_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_52503_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_52503_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_52503_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_52503_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_52503_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()




    #SRI breakdown 1 3197015001050

    sri_gt1_1001_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min0)).count()
    sri_gt1_1001_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min1)).count()
    sri_gt1_1001_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min2)).count()
    sri_gt1_1001_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min3)).count()
    sri_gt1_1001_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min4)).count()
    sri_gt1_1001_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min5)).count()


 #SRI breakdown 2 3197015001050

    sri_gt1_1002_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min0)).count()
    sri_gt1_1002_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min1)).count()
    sri_gt1_1002_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min2)).count()
    sri_gt1_1002_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min3)).count()
    sri_gt1_1002_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min4)).count()
    sri_gt1_1002_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min5)).count()


#SRI breakdown 3 3197015001050

    sri_gt1_1003_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min0)).count()
    sri_gt1_1003_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min1)).count()
    sri_gt1_1003_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min2)).count()
    sri_gt1_1003_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min3)).count()
    sri_gt1_1003_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min4)).count()
    sri_gt1_1003_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min5)).count()


#SRI breakdown 4 3197015001050
    sri_gt1_1004_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min0)).count()
    sri_gt1_1004_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min1)).count()
    sri_gt1_1004_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min2)).count()
    sri_gt1_1004_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min3)).count()
    sri_gt1_1004_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min4)).count()
    sri_gt1_1004_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="3197015001050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min5)).count()




    #SRI breakdown 1 61491500050

    sri_gt2_1001_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min0)).count()
    sri_gt2_1001_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min1)).count()
    sri_gt2_1001_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min2)).count()
    sri_gt2_1001_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min3)).count()
    sri_gt2_1001_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min4)).count()
    sri_gt2_1001_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1001', time__startswith="{}{}".format(get_hour, min5)).count()




    #SRI breakdown 2 61491500050

    sri_gt2_1002_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min0)).count()
    sri_gt2_1002_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min1)).count()
    sri_gt2_1002_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min2)).count()
    sri_gt2_1002_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min3)).count()
    sri_gt2_1002_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min4)).count()
    sri_gt2_1002_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1002', time__startswith="{}{}".format(get_hour, min5)).count()



    #SRI breakdown 3 61491500050

    sri_gt2_1003_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min0)).count()
    sri_gt2_1003_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min1)).count()
    sri_gt2_1003_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min2)).count()
    sri_gt2_1003_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min3)).count()
    sri_gt2_1003_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min4)).count()
    sri_gt2_1003_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1003', time__startswith="{}{}".format(get_hour, min5)).count()



    #SRI breakdown 4 61491500050

    sri_gt2_1004_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min0)).count()
    sri_gt2_1004_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min1)).count()
    sri_gt2_1004_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min2)).count()
    sri_gt2_1004_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min3)).count()
    sri_gt2_1004_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min4)).count()
    sri_gt2_1004_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(msisdn__startswith="65", system__exact="smsc-2-eu4,", error_msg__contains="onDialogTimeoutafterSRIRequest", gt__contains="61491500050,", networkid__contains='1004', time__startswith="{}{}".format(get_hour, min5)).count()



    #FWSM breakdown 1 3197015001050 route TATA

    mtfs_gt1_1001_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1001_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1001_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1001_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1001_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1001_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


    #FWSM breakdown 2 3197015001050 route iBasis

    mtfs_gt1_1002_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1002_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1002_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1002_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1002_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1002_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


#FWSM breakdown 3 3197015001050 route Comfone

    mtfs_gt1_1003_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1003_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1003_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1003_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1003_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1003_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()

#FWSM breakdown 4 3197015001050 route BICS

    mtfs_gt1_1004_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1004_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1004_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1004_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1004_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1004_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


 #FWSM breakdown 1 61491500050 route TATA

    mtfs_gt2_1001_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1001_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1001_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1001_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1001_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1001_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()



    #FWSM breakdown 2 61491500050 route iBasis

    mtfs_gt2_1002_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1002_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1002_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1002_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1002_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1002_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


#FWSM breakdown 3 61491500050 route Comfone

    mtfs_gt2_1003_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1003_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1003_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1003_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1003_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1003_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()

#FWSM breakdown 4 61491500050 route BICS

    mtfs_gt2_1004_min0_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1004_min1_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1004_min2_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1004_min3_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1004_min4_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1004_min5_smsc_2_eu4_0 = CdrProcess.objects.filter(imsi__startswith="52501", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()



    # Text here some text purple 

    #FWSM breakdown 1 3197015001050 route TATA

    mtfs_gt1_1001_min0_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1001_min1_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1001_min2_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1001_min3_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1001_min4_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1001_min5_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


    #FWSM breakdown 2 3197015001050 route iBasis

    mtfs_gt1_1002_min0_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1002_min1_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1002_min2_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1002_min3_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1002_min4_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1002_min5_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


#FWSM breakdown 3 3197015001050 route Comfone

    mtfs_gt1_1003_min0_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1003_min1_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1003_min2_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1003_min3_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1003_min4_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1003_min5_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()

#FWSM breakdown 4 3197015001050 route BICS

    mtfs_gt1_1004_min0_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1004_min1_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1004_min2_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1004_min3_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1004_min4_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1004_min5_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()



    #FWSM breakdown 1 3197015001050 route TATA

    mtfs_gt2_1001_min0_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1001_min1_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1001_min2_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1001_min3_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1001_min4_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1001_min5_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


    #FWSM breakdown 2 3197015001050 route iBasis

    mtfs_gt2_1002_min0_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1002_min1_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1002_min2_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1002_min3_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1002_min4_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1002_min5_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


#FWSM breakdown 3 3197015001050 route Comfone

    mtfs_gt2_1003_min0_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1003_min1_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1003_min2_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1003_min3_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1003_min4_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1003_min5_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()

#FWSM breakdown 4 3197015001050 route BICS

    mtfs_gt2_1004_min0_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1004_min1_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1004_min2_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1004_min3_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1004_min4_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1004_min5_smsc_2_eu4_1 = CdrProcess.objects.filter(imsi__startswith="52505", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()









    # Text here some text purple 

    #FWSM breakdown 1 3197015001050 route TATA

    mtfs_gt1_1001_min0_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1001_min1_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1001_min2_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1001_min3_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1001_min4_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1001_min5_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


    #FWSM breakdown 2 3197015001050 route iBasis

    mtfs_gt1_1002_min0_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1002_min1_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1002_min2_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1002_min3_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1002_min4_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1002_min5_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


#FWSM breakdown 3 3197015001050 route Comfone

    mtfs_gt1_1003_min0_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1003_min1_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1003_min2_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1003_min3_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1003_min4_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1003_min5_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()

#FWSM breakdown 4 3197015001050 route BICS

    mtfs_gt1_1004_min0_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt1_1004_min1_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt1_1004_min2_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt1_1004_min3_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt1_1004_min4_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt1_1004_min5_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="3197015001050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()




    #FWSM breakdown 1 3197015001050 route TATA

    mtfs_gt2_1001_min0_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1001_min1_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1001_min2_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1001_min3_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1001_min4_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1001_min5_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1001', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


    #FWSM breakdown 2 3197015001050 route iBasis

    mtfs_gt2_1002_min0_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1002_min1_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1002_min2_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1002_min3_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1002_min4_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1002_min5_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1002', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()


#FWSM breakdown 3 3197015001050 route Comfone

    mtfs_gt2_1003_min0_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1003_min1_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1003_min2_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1003_min3_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1003_min4_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1003_min5_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1003', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()

#FWSM breakdown 4 3197015001050 route BICS

    mtfs_gt2_1004_min0_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min0)).count()
    mtfs_gt2_1004_min1_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min1)).count()
    mtfs_gt2_1004_min2_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min2)).count()
    mtfs_gt2_1004_min3_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min3)).count()
    mtfs_gt2_1004_min4_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min4)).count()
    mtfs_gt2_1004_min5_smsc_2_eu4_2 = CdrProcess.objects.filter(imsi__startswith="52503", system__exact="smsc-2-eu4,", gt__contains="61491500050,", networkid__contains='1004', error_msg__contains="onDialogTimeoutafterMtForwardSMRequest", time__startswith="{}{}".format(get_hour, min5)).count()







    context = {
        'count_success_smsc_2_eu4' : count_success_smsc_2_eu4,
        'count_temp_failed_smsc_2_eu4' : count_temp_failed_smsc_2_eu4,
        'count_failed_smsc_2_eu4' : count_failed_smsc_2_eu4,

        'total_min0_smsc_2_eu4' : total_min0_smsc_2_eu4,
        'total_min1_smsc_2_eu4' : total_min1_smsc_2_eu4,
        'total_min2_smsc_2_eu4' : total_min2_smsc_2_eu4,
        'total_min3_smsc_2_eu4' : total_min3_smsc_2_eu4,
        'total_min4_smsc_2_eu4' : total_min4_smsc_2_eu4,
        'total_min5_smsc_2_eu4' : total_min5_smsc_2_eu4,

        'success_min0_smsc_2_eu4' : success_min0_smsc_2_eu4,
        'success_min1_smsc_2_eu4' : success_min1_smsc_2_eu4,
        'success_min2_smsc_2_eu4' : success_min2_smsc_2_eu4,
        'success_min3_smsc_2_eu4' : success_min3_smsc_2_eu4,
        'success_min4_smsc_2_eu4' : success_min4_smsc_2_eu4,
        'success_min5_smsc_2_eu4' : success_min5_smsc_2_eu4,

        'failed_min0_smsc_2_eu4' : failed_min0_smsc_2_eu4,
        'failed_min1_smsc_2_eu4' : failed_min1_smsc_2_eu4,
        'failed_min2_smsc_2_eu4' : failed_min2_smsc_2_eu4,
        'failed_min3_smsc_2_eu4' : failed_min3_smsc_2_eu4,
        'failed_min4_smsc_2_eu4' : failed_min4_smsc_2_eu4,
        'failed_min5_smsc_2_eu4' : failed_min5_smsc_2_eu4,

        'sri_min0_smsc_2_eu4' : sri_min0_smsc_2_eu4,
        'sri_min1_smsc_2_eu4' : sri_min1_smsc_2_eu4,
        'sri_min2_smsc_2_eu4' : sri_min2_smsc_2_eu4,
        'sri_min3_smsc_2_eu4' : sri_min3_smsc_2_eu4,
        'sri_min4_smsc_2_eu4' : sri_min4_smsc_2_eu4,
        'sri_min5_smsc_2_eu4' : sri_min5_smsc_2_eu4,

        'mtfs_min0_smsc_2_eu4' : mtfs_min0_smsc_2_eu4,
        'mtfs_min1_smsc_2_eu4' : mtfs_min1_smsc_2_eu4,
        'mtfs_min2_smsc_2_eu4' : mtfs_min2_smsc_2_eu4,
        'mtfs_min3_smsc_2_eu4' : mtfs_min3_smsc_2_eu4,
        'mtfs_min4_smsc_2_eu4' : mtfs_min4_smsc_2_eu4,
        'mtfs_min5_smsc_2_eu4' : mtfs_min5_smsc_2_eu4,

        'mtfs_min0_smsc_2_eu4_1' : mtfs_min0_smsc_2_eu4_1, 
        'mtfs_min1_smsc_2_eu4_1' : mtfs_min1_smsc_2_eu4_1, 
        'mtfs_min2_smsc_2_eu4_1' : mtfs_min2_smsc_2_eu4_1, 
        'mtfs_min3_smsc_2_eu4_1' : mtfs_min3_smsc_2_eu4_1, 
        'mtfs_min4_smsc_2_eu4_1' : mtfs_min4_smsc_2_eu4_1, 
        'mtfs_min5_smsc_2_eu4_1' : mtfs_min5_smsc_2_eu4_1, 

        'mtfs_52503_min0_smsc_2_eu4_0' : mtfs_52503_min0_smsc_2_eu4_0,
        'mtfs_52503_min1_smsc_2_eu4_0' : mtfs_52503_min1_smsc_2_eu4_0,
        'mtfs_52503_min2_smsc_2_eu4_0' : mtfs_52503_min2_smsc_2_eu4_0,
        'mtfs_52503_min3_smsc_2_eu4_0' : mtfs_52503_min3_smsc_2_eu4_0,
        'mtfs_52503_min4_smsc_2_eu4_0' : mtfs_52503_min4_smsc_2_eu4_0,
        'mtfs_52503_min5_smsc_2_eu4_0' : mtfs_52503_min5_smsc_2_eu4_0,


        'sri_gt1_1001_min0_smsc_2_eu4_0' : sri_gt1_1001_min0_smsc_2_eu4_0,
        'sri_gt1_1001_min1_smsc_2_eu4_0' : sri_gt1_1001_min1_smsc_2_eu4_0,
        'sri_gt1_1001_min2_smsc_2_eu4_0' : sri_gt1_1001_min2_smsc_2_eu4_0,
        'sri_gt1_1001_min3_smsc_2_eu4_0' : sri_gt1_1001_min3_smsc_2_eu4_0,
        'sri_gt1_1001_min4_smsc_2_eu4_0' : sri_gt1_1001_min4_smsc_2_eu4_0,
        'sri_gt1_1001_min5_smsc_2_eu4_0' : sri_gt1_1001_min5_smsc_2_eu4_0,

        'sri_gt1_1002_min0_smsc_2_eu4_0' : sri_gt1_1002_min0_smsc_2_eu4_0,
        'sri_gt1_1002_min1_smsc_2_eu4_0' : sri_gt1_1002_min1_smsc_2_eu4_0,
        'sri_gt1_1002_min2_smsc_2_eu4_0' : sri_gt1_1002_min2_smsc_2_eu4_0,
        'sri_gt1_1002_min3_smsc_2_eu4_0' : sri_gt1_1002_min3_smsc_2_eu4_0,
        'sri_gt1_1002_min4_smsc_2_eu4_0' : sri_gt1_1002_min4_smsc_2_eu4_0,
        'sri_gt1_1002_min5_smsc_2_eu4_0' : sri_gt1_1002_min5_smsc_2_eu4_0,


        'sri_gt1_1003_min0_smsc_2_eu4_0' : sri_gt1_1003_min0_smsc_2_eu4_0, 
        'sri_gt1_1003_min1_smsc_2_eu4_0' : sri_gt1_1003_min1_smsc_2_eu4_0, 
        'sri_gt1_1003_min2_smsc_2_eu4_0' : sri_gt1_1003_min2_smsc_2_eu4_0, 
        'sri_gt1_1003_min3_smsc_2_eu4_0' : sri_gt1_1003_min3_smsc_2_eu4_0, 
        'sri_gt1_1003_min4_smsc_2_eu4_0' : sri_gt1_1003_min4_smsc_2_eu4_0, 
        'sri_gt1_1003_min5_smsc_2_eu4_0' : sri_gt1_1003_min5_smsc_2_eu4_0, 

        'sri_gt1_1004_min0_smsc_2_eu4_0' : sri_gt1_1004_min0_smsc_2_eu4_0,
        'sri_gt1_1004_min1_smsc_2_eu4_0' : sri_gt1_1004_min1_smsc_2_eu4_0,
        'sri_gt1_1004_min2_smsc_2_eu4_0' : sri_gt1_1004_min2_smsc_2_eu4_0,
        'sri_gt1_1004_min3_smsc_2_eu4_0' : sri_gt1_1004_min3_smsc_2_eu4_0,
        'sri_gt1_1004_min4_smsc_2_eu4_0' : sri_gt1_1004_min4_smsc_2_eu4_0,
        'sri_gt1_1004_min5_smsc_2_eu4_0' : sri_gt1_1004_min5_smsc_2_eu4_0,


        'sri_gt2_1001_min0_smsc_2_eu4_0' : sri_gt2_1001_min0_smsc_2_eu4_0,
        'sri_gt2_1001_min1_smsc_2_eu4_0' : sri_gt2_1001_min1_smsc_2_eu4_0,
        'sri_gt2_1001_min2_smsc_2_eu4_0' : sri_gt2_1001_min2_smsc_2_eu4_0,
        'sri_gt2_1001_min3_smsc_2_eu4_0' : sri_gt2_1001_min3_smsc_2_eu4_0,
        'sri_gt2_1001_min4_smsc_2_eu4_0' : sri_gt2_1001_min4_smsc_2_eu4_0,
        'sri_gt2_1001_min5_smsc_2_eu4_0' : sri_gt2_1001_min5_smsc_2_eu4_0,


        'sri_gt2_1002_min0_smsc_2_eu4_0' : sri_gt2_1002_min0_smsc_2_eu4_0,
        'sri_gt2_1002_min1_smsc_2_eu4_0' : sri_gt2_1002_min1_smsc_2_eu4_0,
        'sri_gt2_1002_min2_smsc_2_eu4_0' : sri_gt2_1002_min2_smsc_2_eu4_0,
        'sri_gt2_1002_min3_smsc_2_eu4_0' : sri_gt2_1002_min3_smsc_2_eu4_0,
        'sri_gt2_1002_min4_smsc_2_eu4_0' : sri_gt2_1002_min4_smsc_2_eu4_0,
        'sri_gt2_1002_min5_smsc_2_eu4_0' : sri_gt2_1002_min5_smsc_2_eu4_0,


        'sri_gt2_1003_min0_smsc_2_eu4_0' : sri_gt2_1003_min0_smsc_2_eu4_0,
        'sri_gt2_1003_min1_smsc_2_eu4_0' : sri_gt2_1003_min1_smsc_2_eu4_0,
        'sri_gt2_1003_min2_smsc_2_eu4_0' : sri_gt2_1003_min2_smsc_2_eu4_0,
        'sri_gt2_1003_min3_smsc_2_eu4_0' : sri_gt2_1003_min3_smsc_2_eu4_0,
        'sri_gt2_1003_min4_smsc_2_eu4_0' : sri_gt2_1003_min4_smsc_2_eu4_0,
        'sri_gt2_1003_min5_smsc_2_eu4_0' : sri_gt2_1003_min5_smsc_2_eu4_0,

        'sri_gt2_1004_min0_smsc_2_eu4_0' : sri_gt2_1004_min0_smsc_2_eu4_0,
        'sri_gt2_1004_min1_smsc_2_eu4_0' : sri_gt2_1004_min1_smsc_2_eu4_0,
        'sri_gt2_1004_min2_smsc_2_eu4_0' : sri_gt2_1004_min2_smsc_2_eu4_0,
        'sri_gt2_1004_min3_smsc_2_eu4_0' : sri_gt2_1004_min3_smsc_2_eu4_0,
        'sri_gt2_1004_min4_smsc_2_eu4_0' : sri_gt2_1004_min4_smsc_2_eu4_0,
        'sri_gt2_1004_min5_smsc_2_eu4_0' : sri_gt2_1004_min5_smsc_2_eu4_0,

        'mtfs_gt1_1001_min0_smsc_2_eu4_0' : mtfs_gt1_1001_min0_smsc_2_eu4_0,
        'mtfs_gt1_1001_min1_smsc_2_eu4_0' : mtfs_gt1_1001_min1_smsc_2_eu4_0,
        'mtfs_gt1_1001_min2_smsc_2_eu4_0' : mtfs_gt1_1001_min2_smsc_2_eu4_0,
        'mtfs_gt1_1001_min3_smsc_2_eu4_0' : mtfs_gt1_1001_min3_smsc_2_eu4_0,
        'mtfs_gt1_1001_min4_smsc_2_eu4_0' : mtfs_gt1_1001_min4_smsc_2_eu4_0,
        'mtfs_gt1_1001_min5_smsc_2_eu4_0' : mtfs_gt1_1001_min5_smsc_2_eu4_0,


        'mtfs_gt1_1002_min0_smsc_2_eu4_0' : mtfs_gt1_1002_min0_smsc_2_eu4_0,
        'mtfs_gt1_1002_min1_smsc_2_eu4_0' : mtfs_gt1_1002_min1_smsc_2_eu4_0,
        'mtfs_gt1_1002_min2_smsc_2_eu4_0' : mtfs_gt1_1002_min2_smsc_2_eu4_0,
        'mtfs_gt1_1002_min3_smsc_2_eu4_0' : mtfs_gt1_1002_min3_smsc_2_eu4_0,
        'mtfs_gt1_1002_min4_smsc_2_eu4_0' : mtfs_gt1_1002_min4_smsc_2_eu4_0,
        'mtfs_gt1_1002_min5_smsc_2_eu4_0' : mtfs_gt1_1002_min5_smsc_2_eu4_0,

        'mtfs_gt1_1003_min0_smsc_2_eu4_0' : mtfs_gt1_1003_min0_smsc_2_eu4_0,
        'mtfs_gt1_1003_min1_smsc_2_eu4_0' : mtfs_gt1_1003_min1_smsc_2_eu4_0,
        'mtfs_gt1_1003_min2_smsc_2_eu4_0' : mtfs_gt1_1003_min2_smsc_2_eu4_0,
        'mtfs_gt1_1003_min3_smsc_2_eu4_0' : mtfs_gt1_1003_min3_smsc_2_eu4_0,
        'mtfs_gt1_1003_min4_smsc_2_eu4_0' : mtfs_gt1_1003_min4_smsc_2_eu4_0,
        'mtfs_gt1_1003_min5_smsc_2_eu4_0' : mtfs_gt1_1003_min5_smsc_2_eu4_0,

        'mtfs_gt1_1004_min0_smsc_2_eu4_0' : mtfs_gt1_1004_min0_smsc_2_eu4_0,
        'mtfs_gt1_1004_min1_smsc_2_eu4_0' : mtfs_gt1_1004_min1_smsc_2_eu4_0,
        'mtfs_gt1_1004_min2_smsc_2_eu4_0' : mtfs_gt1_1004_min2_smsc_2_eu4_0,
        'mtfs_gt1_1004_min3_smsc_2_eu4_0' : mtfs_gt1_1004_min3_smsc_2_eu4_0,
        'mtfs_gt1_1004_min4_smsc_2_eu4_0' : mtfs_gt1_1004_min4_smsc_2_eu4_0,
        'mtfs_gt1_1004_min5_smsc_2_eu4_0' : mtfs_gt1_1004_min5_smsc_2_eu4_0,


        'mtfs_gt2_1001_min0_smsc_2_eu4_0' : mtfs_gt2_1001_min0_smsc_2_eu4_0,
        'mtfs_gt2_1001_min1_smsc_2_eu4_0' : mtfs_gt2_1001_min1_smsc_2_eu4_0,
        'mtfs_gt2_1001_min2_smsc_2_eu4_0' : mtfs_gt2_1001_min2_smsc_2_eu4_0,
        'mtfs_gt2_1001_min3_smsc_2_eu4_0' : mtfs_gt2_1001_min3_smsc_2_eu4_0,
        'mtfs_gt2_1001_min4_smsc_2_eu4_0' : mtfs_gt2_1001_min4_smsc_2_eu4_0,
        'mtfs_gt2_1001_min5_smsc_2_eu4_0' : mtfs_gt2_1001_min5_smsc_2_eu4_0,

        'mtfs_gt2_1002_min0_smsc_2_eu4_0' : mtfs_gt2_1002_min0_smsc_2_eu4_0,
        'mtfs_gt2_1002_min1_smsc_2_eu4_0' : mtfs_gt2_1002_min1_smsc_2_eu4_0,
        'mtfs_gt2_1002_min2_smsc_2_eu4_0' : mtfs_gt2_1002_min2_smsc_2_eu4_0,
        'mtfs_gt2_1002_min3_smsc_2_eu4_0' : mtfs_gt2_1002_min3_smsc_2_eu4_0,
        'mtfs_gt2_1002_min4_smsc_2_eu4_0' : mtfs_gt2_1002_min4_smsc_2_eu4_0,
        'mtfs_gt2_1002_min5_smsc_2_eu4_0' : mtfs_gt2_1002_min5_smsc_2_eu4_0,

        'mtfs_gt2_1003_min0_smsc_2_eu4_0' : mtfs_gt2_1003_min0_smsc_2_eu4_0,
        'mtfs_gt2_1003_min1_smsc_2_eu4_0' : mtfs_gt2_1003_min1_smsc_2_eu4_0,
        'mtfs_gt2_1003_min2_smsc_2_eu4_0' : mtfs_gt2_1003_min2_smsc_2_eu4_0,
        'mtfs_gt2_1003_min3_smsc_2_eu4_0' : mtfs_gt2_1003_min3_smsc_2_eu4_0,
        'mtfs_gt2_1003_min4_smsc_2_eu4_0' : mtfs_gt2_1003_min4_smsc_2_eu4_0,
        'mtfs_gt2_1003_min5_smsc_2_eu4_0' : mtfs_gt2_1003_min5_smsc_2_eu4_0,

        'mtfs_gt2_1004_min0_smsc_2_eu4_0' : mtfs_gt2_1004_min0_smsc_2_eu4_0,
        'mtfs_gt2_1004_min1_smsc_2_eu4_0' : mtfs_gt2_1004_min1_smsc_2_eu4_0,
        'mtfs_gt2_1004_min2_smsc_2_eu4_0' : mtfs_gt2_1004_min2_smsc_2_eu4_0,
        'mtfs_gt2_1004_min3_smsc_2_eu4_0' : mtfs_gt2_1004_min3_smsc_2_eu4_0,
        'mtfs_gt2_1004_min4_smsc_2_eu4_0' : mtfs_gt2_1004_min4_smsc_2_eu4_0,
        'mtfs_gt2_1004_min5_smsc_2_eu4_0' : mtfs_gt2_1004_min5_smsc_2_eu4_0,



        'mtfs_gt1_1001_min0_smsc_2_eu4_1' : mtfs_gt1_1001_min0_smsc_2_eu4_1,
        'mtfs_gt1_1001_min1_smsc_2_eu4_1' : mtfs_gt1_1001_min1_smsc_2_eu4_1,
        'mtfs_gt1_1001_min2_smsc_2_eu4_1' : mtfs_gt1_1001_min2_smsc_2_eu4_1,
        'mtfs_gt1_1001_min3_smsc_2_eu4_1' : mtfs_gt1_1001_min3_smsc_2_eu4_1,
        'mtfs_gt1_1001_min4_smsc_2_eu4_1' : mtfs_gt1_1001_min4_smsc_2_eu4_1,
        'mtfs_gt1_1001_min5_smsc_2_eu4_1' : mtfs_gt1_1001_min5_smsc_2_eu4_1,

        'mtfs_gt1_1002_min0_smsc_2_eu4_1' : mtfs_gt1_1002_min0_smsc_2_eu4_1,
        'mtfs_gt1_1002_min1_smsc_2_eu4_1' : mtfs_gt1_1002_min1_smsc_2_eu4_1,
        'mtfs_gt1_1002_min2_smsc_2_eu4_1' : mtfs_gt1_1002_min2_smsc_2_eu4_1,
        'mtfs_gt1_1002_min3_smsc_2_eu4_1' : mtfs_gt1_1002_min3_smsc_2_eu4_1,
        'mtfs_gt1_1002_min4_smsc_2_eu4_1' : mtfs_gt1_1002_min4_smsc_2_eu4_1,
        'mtfs_gt1_1002_min5_smsc_2_eu4_1' : mtfs_gt1_1002_min5_smsc_2_eu4_1,

        'mtfs_gt1_1003_min0_smsc_2_eu4_1' : mtfs_gt1_1003_min0_smsc_2_eu4_1,
        'mtfs_gt1_1003_min1_smsc_2_eu4_1' : mtfs_gt1_1003_min1_smsc_2_eu4_1,
        'mtfs_gt1_1003_min2_smsc_2_eu4_1' : mtfs_gt1_1003_min2_smsc_2_eu4_1,
        'mtfs_gt1_1003_min3_smsc_2_eu4_1' : mtfs_gt1_1003_min3_smsc_2_eu4_1,
        'mtfs_gt1_1003_min4_smsc_2_eu4_1' : mtfs_gt1_1003_min4_smsc_2_eu4_1,
        'mtfs_gt1_1003_min5_smsc_2_eu4_1' : mtfs_gt1_1003_min5_smsc_2_eu4_1,

        'mtfs_gt1_1004_min0_smsc_2_eu4_1' : mtfs_gt1_1004_min0_smsc_2_eu4_1,
        'mtfs_gt1_1004_min1_smsc_2_eu4_1' : mtfs_gt1_1004_min1_smsc_2_eu4_1,
        'mtfs_gt1_1004_min2_smsc_2_eu4_1' : mtfs_gt1_1004_min2_smsc_2_eu4_1,
        'mtfs_gt1_1004_min3_smsc_2_eu4_1' : mtfs_gt1_1004_min3_smsc_2_eu4_1,
        'mtfs_gt1_1004_min4_smsc_2_eu4_1' : mtfs_gt1_1004_min4_smsc_2_eu4_1,
        'mtfs_gt1_1004_min5_smsc_2_eu4_1' : mtfs_gt1_1004_min5_smsc_2_eu4_1,



        'mtfs_gt2_1001_min0_smsc_2_eu4_1' : mtfs_gt2_1001_min0_smsc_2_eu4_1,
        'mtfs_gt2_1001_min1_smsc_2_eu4_1' : mtfs_gt2_1001_min1_smsc_2_eu4_1,
        'mtfs_gt2_1001_min2_smsc_2_eu4_1' : mtfs_gt2_1001_min2_smsc_2_eu4_1,
        'mtfs_gt2_1001_min3_smsc_2_eu4_1' : mtfs_gt2_1001_min3_smsc_2_eu4_1,
        'mtfs_gt2_1001_min4_smsc_2_eu4_1' : mtfs_gt2_1001_min4_smsc_2_eu4_1,
        'mtfs_gt2_1001_min5_smsc_2_eu4_1' : mtfs_gt2_1001_min5_smsc_2_eu4_1,

        'mtfs_gt2_1002_min0_smsc_2_eu4_1' : mtfs_gt2_1002_min0_smsc_2_eu4_1,
        'mtfs_gt2_1002_min1_smsc_2_eu4_1' : mtfs_gt2_1002_min1_smsc_2_eu4_1,
        'mtfs_gt2_1002_min2_smsc_2_eu4_1' : mtfs_gt2_1002_min2_smsc_2_eu4_1,
        'mtfs_gt2_1002_min3_smsc_2_eu4_1' : mtfs_gt2_1002_min3_smsc_2_eu4_1,
        'mtfs_gt2_1002_min4_smsc_2_eu4_1' : mtfs_gt2_1002_min4_smsc_2_eu4_1,
        'mtfs_gt2_1002_min5_smsc_2_eu4_1' : mtfs_gt2_1002_min5_smsc_2_eu4_1,

        'mtfs_gt2_1003_min0_smsc_2_eu4_1' : mtfs_gt2_1003_min0_smsc_2_eu4_1,
        'mtfs_gt2_1003_min1_smsc_2_eu4_1' : mtfs_gt2_1003_min1_smsc_2_eu4_1,
        'mtfs_gt2_1003_min2_smsc_2_eu4_1' : mtfs_gt2_1003_min2_smsc_2_eu4_1,
        'mtfs_gt2_1003_min3_smsc_2_eu4_1' : mtfs_gt2_1003_min3_smsc_2_eu4_1,
        'mtfs_gt2_1003_min4_smsc_2_eu4_1' : mtfs_gt2_1003_min4_smsc_2_eu4_1,
        'mtfs_gt2_1003_min5_smsc_2_eu4_1' : mtfs_gt2_1003_min5_smsc_2_eu4_1,

        'mtfs_gt2_1004_min0_smsc_2_eu4_1' : mtfs_gt2_1004_min0_smsc_2_eu4_1,
        'mtfs_gt2_1004_min1_smsc_2_eu4_1' : mtfs_gt2_1004_min1_smsc_2_eu4_1,
        'mtfs_gt2_1004_min2_smsc_2_eu4_1' : mtfs_gt2_1004_min2_smsc_2_eu4_1,
        'mtfs_gt2_1004_min3_smsc_2_eu4_1' : mtfs_gt2_1004_min3_smsc_2_eu4_1,
        'mtfs_gt2_1004_min4_smsc_2_eu4_1' : mtfs_gt2_1004_min4_smsc_2_eu4_1,
        'mtfs_gt2_1004_min5_smsc_2_eu4_1' : mtfs_gt2_1004_min5_smsc_2_eu4_1,







        'mtfs_gt1_1001_min0_smsc_2_eu4_2' : mtfs_gt1_1001_min0_smsc_2_eu4_2,
        'mtfs_gt1_1001_min1_smsc_2_eu4_2' : mtfs_gt1_1001_min1_smsc_2_eu4_2,
        'mtfs_gt1_1001_min2_smsc_2_eu4_2' : mtfs_gt1_1001_min2_smsc_2_eu4_2,
        'mtfs_gt1_1001_min3_smsc_2_eu4_2' : mtfs_gt1_1001_min3_smsc_2_eu4_2,
        'mtfs_gt1_1001_min4_smsc_2_eu4_2' : mtfs_gt1_1001_min4_smsc_2_eu4_2,
        'mtfs_gt1_1001_min5_smsc_2_eu4_2' : mtfs_gt1_1001_min5_smsc_2_eu4_2,

        'mtfs_gt1_1002_min0_smsc_2_eu4_2' : mtfs_gt1_1002_min0_smsc_2_eu4_2,
        'mtfs_gt1_1002_min1_smsc_2_eu4_2' : mtfs_gt1_1002_min1_smsc_2_eu4_2,
        'mtfs_gt1_1002_min2_smsc_2_eu4_2' : mtfs_gt1_1002_min2_smsc_2_eu4_2,
        'mtfs_gt1_1002_min3_smsc_2_eu4_2' : mtfs_gt1_1002_min3_smsc_2_eu4_2,
        'mtfs_gt1_1002_min4_smsc_2_eu4_2' : mtfs_gt1_1002_min4_smsc_2_eu4_2,
        'mtfs_gt1_1002_min5_smsc_2_eu4_2' : mtfs_gt1_1002_min5_smsc_2_eu4_2,

        'mtfs_gt1_1003_min0_smsc_2_eu4_2' : mtfs_gt1_1003_min0_smsc_2_eu4_2,
        'mtfs_gt1_1003_min1_smsc_2_eu4_2' : mtfs_gt1_1003_min1_smsc_2_eu4_2,
        'mtfs_gt1_1003_min2_smsc_2_eu4_2' : mtfs_gt1_1003_min2_smsc_2_eu4_2,
        'mtfs_gt1_1003_min3_smsc_2_eu4_2' : mtfs_gt1_1003_min3_smsc_2_eu4_2,
        'mtfs_gt1_1003_min4_smsc_2_eu4_2' : mtfs_gt1_1003_min4_smsc_2_eu4_2,
        'mtfs_gt1_1003_min5_smsc_2_eu4_2' : mtfs_gt1_1003_min5_smsc_2_eu4_2,

        'mtfs_gt1_1004_min0_smsc_2_eu4_2' : mtfs_gt1_1004_min0_smsc_2_eu4_2,
        'mtfs_gt1_1004_min1_smsc_2_eu4_2' : mtfs_gt1_1004_min1_smsc_2_eu4_2,
        'mtfs_gt1_1004_min2_smsc_2_eu4_2' : mtfs_gt1_1004_min2_smsc_2_eu4_2,
        'mtfs_gt1_1004_min3_smsc_2_eu4_2' : mtfs_gt1_1004_min3_smsc_2_eu4_2,
        'mtfs_gt1_1004_min4_smsc_2_eu4_2' : mtfs_gt1_1004_min4_smsc_2_eu4_2,
        'mtfs_gt1_1004_min5_smsc_2_eu4_2' : mtfs_gt1_1004_min5_smsc_2_eu4_2,



        'mtfs_gt2_1001_min0_smsc_2_eu4_2' : mtfs_gt2_1001_min0_smsc_2_eu4_2,
        'mtfs_gt2_1001_min1_smsc_2_eu4_2' : mtfs_gt2_1001_min1_smsc_2_eu4_2,
        'mtfs_gt2_1001_min2_smsc_2_eu4_2' : mtfs_gt2_1001_min2_smsc_2_eu4_2,
        'mtfs_gt2_1001_min3_smsc_2_eu4_2' : mtfs_gt2_1001_min3_smsc_2_eu4_2,
        'mtfs_gt2_1001_min4_smsc_2_eu4_2' : mtfs_gt2_1001_min4_smsc_2_eu4_2,
        'mtfs_gt2_1001_min5_smsc_2_eu4_2' : mtfs_gt2_1001_min5_smsc_2_eu4_2,

        'mtfs_gt2_1002_min0_smsc_2_eu4_2' : mtfs_gt2_1002_min0_smsc_2_eu4_2,
        'mtfs_gt2_1002_min1_smsc_2_eu4_2' : mtfs_gt2_1002_min1_smsc_2_eu4_2,
        'mtfs_gt2_1002_min2_smsc_2_eu4_2' : mtfs_gt2_1002_min2_smsc_2_eu4_2,
        'mtfs_gt2_1002_min3_smsc_2_eu4_2' : mtfs_gt2_1002_min3_smsc_2_eu4_2,
        'mtfs_gt2_1002_min4_smsc_2_eu4_2' : mtfs_gt2_1002_min4_smsc_2_eu4_2,
        'mtfs_gt2_1002_min5_smsc_2_eu4_2' : mtfs_gt2_1002_min5_smsc_2_eu4_2,

        'mtfs_gt2_1003_min0_smsc_2_eu4_2' : mtfs_gt2_1003_min0_smsc_2_eu4_2,
        'mtfs_gt2_1003_min1_smsc_2_eu4_2' : mtfs_gt2_1003_min1_smsc_2_eu4_2,
        'mtfs_gt2_1003_min2_smsc_2_eu4_2' : mtfs_gt2_1003_min2_smsc_2_eu4_2,
        'mtfs_gt2_1003_min3_smsc_2_eu4_2' : mtfs_gt2_1003_min3_smsc_2_eu4_2,
        'mtfs_gt2_1003_min4_smsc_2_eu4_2' : mtfs_gt2_1003_min4_smsc_2_eu4_2,
        'mtfs_gt2_1003_min5_smsc_2_eu4_2' : mtfs_gt2_1003_min5_smsc_2_eu4_2,

        'mtfs_gt2_1004_min0_smsc_2_eu4_2' : mtfs_gt2_1004_min0_smsc_2_eu4_2,
        'mtfs_gt2_1004_min1_smsc_2_eu4_2' : mtfs_gt2_1004_min1_smsc_2_eu4_2,
        'mtfs_gt2_1004_min2_smsc_2_eu4_2' : mtfs_gt2_1004_min2_smsc_2_eu4_2,
        'mtfs_gt2_1004_min3_smsc_2_eu4_2' : mtfs_gt2_1004_min3_smsc_2_eu4_2,
        'mtfs_gt2_1004_min4_smsc_2_eu4_2' : mtfs_gt2_1004_min4_smsc_2_eu4_2,
        'mtfs_gt2_1004_min5_smsc_2_eu4_2' : mtfs_gt2_1004_min5_smsc_2_eu4_2,


        'final_time' : final_time,
        'get_hour' : get_hour,
        'count_total_smsc_2_eu4' : count_total_smsc_2_eu4,

        'min0' : min0,
        'min1' : min1,
        'min2' : min2,
        'min3' : min3,
        'min4' : min4,
        'min5' : min5


    }
    return render(request, "crm/dashboard.html", context)
