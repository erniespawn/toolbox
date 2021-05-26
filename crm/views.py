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
from crm.models import CdrProcess, row1_1
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
            q = CdrProcess(time="00:00:00.000,", date='1999-99-99', msisdn='9999') # Insert 1 default record in DB and save it
            q.save()
            return render(request, "crm/smsc.html", {})

        elif request.POST.get("insertDB") == 'insertDB':
            insertDB = request.POST.get("insertDB")
            con = sqlite3.connect('db.sqlite3')
            cur = con.cursor()

            ccsg = '65'
            gt_sg1= '3197015001050'
            gt_sg1= '61491500050'

            ccms = '91'
            gt_6995 = '3197015001050,'
            gt_6994 = '3197015001052,'
            smsc1 = 'smsc-1-eu1,'
            smsc2 = 'smsc-2-eu1,'
            smsc3 = 'smsc-1-eu4,'
            smsc4 = 'smsc-2-eu4,'
            success = 'success,'
            partial = 'partial,'
            failed = 'failed,'
            temp_failed = 'temp_failed,'

            s1 = list2hourv2()
            print ("effe testen {}".format(s1))

            r1 = list2hourv2()
            for x in r1:
                # Row 1
                r2 = ("{}:{}".format(x[0], x[1]))
                print (r2)
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and status IN ('failed,', 'success,', 'temp_failed,')".format(gt_6994, r2, ccms))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', '1a');".format(r2, result1[0])) #insert only time and total
                con.commit()
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and status='success,'".format(gt_6994, r2, ccms))
                result1 = cur.fetchone()
                cur.execute(" UPDATE crm_row1_1 SET success = '{}' WHERE time like '{}%' and user_id = '1a';".format(result1[0], r2))
                con.commit()
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and status IN ('failed,', 'temp_failed,')".format(gt_6994, r2, ccms))
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = '1a';".format(result1[0], r2))
                con.commit()

                # Row 1 column 2/3
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'onDialogTimeoutafterSRIRequest'".format(gt_6994, r2, ccms, smsc4))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', '1b');".format(r2, result1[0])) #insert row 1 column 2 SRI timeout
                con.commit()
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'onDialogTimeoutafterMtForwardSMRequest'".format(gt_6994, r2, ccms, smsc4))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', '1c');".format(r2, result1[0])) #insert row 1 column 3 MT timeout
                con.commit()

                # Row 1 column 3 extra error added (sys_fail)
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:'".format(gt_6994, r2, ccms, smsc4))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = '1c';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 1 column 4/5
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'onDialogTimeoutafterSRIRequest'".format(gt_6994, r2, ccms, smsc2))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', '1d');".format(r2, result1[0])) #insert row 1 column 4 SRI timeout
                con.commit()
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'onDialogTimeoutafterMtForwardSMRequest'".format(gt_6994, r2, ccms, smsc2))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', '1e');".format(r2, result1[0])) #insert row 1 column 5 MT timeout
                con.commit()

                # Row 1 column 5 extra error added (sys_fail)
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:'".format(gt_6994, r2, ccms, smsc2))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = '1e';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()




                # Row 2
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and status IN ('failed,', 'success,', 'temp_failed,', 'partial,')".format(gt_6995, r2, ccms))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', '2a');".format(r2, result1[0])) #insert only time and total
                con.commit()

                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and status='success,'".format(gt_6995, r2, ccms))
                result1 = cur.fetchone()
                cur.execute(" UPDATE crm_row1_1 SET success = '{}' WHERE time like '{}%' and user_id = '2a';".format(result1[0], r2))
                con.commit()

                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and status IN ('failed,', 'temp_failed,')".format(gt_6995, r2, ccms))
                result1 = cur.fetchone()
                cur.execute(" UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = '2a';".format(result1[0], r2))
                con.commit()

                # Row 2 column 2/3
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'onDialogTimeoutafterSRIRequest'".format(gt_6995, r2, ccms, smsc2))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', '2b');".format(r2, result1[0])) #insert row 2 column 2 SRI timeout
                con.commit()
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'onDialogTimeoutafterMtForwardSMRequest'".format(gt_6995, r2, ccms, smsc2))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', '2c');".format(r2, result1[0])) #insert row 2 column 3 MT timeout
                con.commit()

                # Row 2 column 3 extra error added (sys_fail)
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:'".format(gt_6995, r2, ccms, smsc2))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = '2c';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 2 column 4/5
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'onDialogTimeoutafterSRIRequest'".format(gt_6995, r2, ccms, smsc4))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', '2d');".format(r2, result1[0])) #insert row 2 column 4 SRI timeout
                con.commit()
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'onDialogTimeoutafterMtForwardSMRequest'".format(gt_6995, r2, ccms, smsc4))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', '2e');".format(r2, result1[0])) #insert row 2 column 5 MT timeout
                con.commit()

                # Row 2 column 5 extra error added (sys_fail)
                cur.execute("SELECT count(*) FROM crm_cdrprocess where gt = '{}' and time like '{}%' and msisdn like '{}%' and system = '{}' and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:'".format(gt_6995, r2, ccms, smsc4))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = '2e';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()




                ## SG new version row 1
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and status IN ('failed,', 'success,', 'temp_failed,')".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("INSERT INTO crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', 'sg_1a');".format(r2, result1[0])) #insert only time and total
                con.commit()

                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and status='success,'".format(r2, ccsg))
                result1 = cur.fetchone()
                cur.execute(" UPDATE crm_row1_1 SET success = '{}' WHERE time like '{}%' and user_id = 'sg_1a';".format(result1[0], r2))
                con.commit()

                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and status IN ('failed,', 'temp_failed,')".format(r2, ccsg))
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_1a';".format(result1[0], r2))
                con.commit()

                # Row 1 column 2/3
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and error_msg = 'onDialogTimeoutafterSRIRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '3', '4', 'sg_1b');".format(r2, result1[0])) #insert row 1 column 2 SRI timeout
                con.commit()
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and imsi like '52501%' and error_msg = 'onDialogTimeoutafterMtForwardSMRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_1c');".format(r2, result1[0])) #insert row 1 column 3 MT timeout
                con.commit()
                # Row 1 column 3 extra error added (sys_fail)
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and imsi like '52501%' and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_1c';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.

                # Row 1 column 4
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and imsi like '52503%' and error_msg = 'onDialogTimeoutafterMtForwardSMRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_1d');".format(r2, result1[0])) #insert row 1 column 3 MT timeout
                con.commit()
                # Row 1 column 3 extra error added (sys_fail)
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and imsi like '52503%' and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_1d';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 1 column 5
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and imsi like '52505%' and error_msg = 'onDialogTimeoutafterMtForwardSMRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_1e');".format(r2, result1[0])) #insert row 1 column 3 MT timeout
                con.commit()
                # Row 1 column 3 extra error added (sys_fail)
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and imsi like '52505%' and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_1e';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()


                # Row 2 column 1 SRI_TO GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'onDialogTimeoutafterSRIRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_2a');".format(r2, result1[0]))
                con.commit()
                # Row 2 column 2 SRI_TO GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'onDialogTimeoutafterSRIRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_2b');".format(r2, result1[0]))
                con.commit()
                # Row 2 column 3 SRI_TO GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'onDialogTimeoutafterSRIRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_2c');".format(r2, result1[0]))
                con.commit()
                # Row 2 column 4 SRI_TO GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'onDialogTimeoutafterSRIRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_2d');".format(r2, result1[0]))
                con.commit()


                # Row 3 column 1 SRI_TO GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'onDialogTimeoutafterSRIRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_3a');".format(r2, result1[0]))
                con.commit()
                # Row 3 column 2 SRI_TO GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'onDialogTimeoutafterSRIRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_3b');".format(r2, result1[0]))
                con.commit()
                # Row 3 column 3 SRI_TO GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'onDialogTimeoutafterSRIRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_3c');".format(r2, result1[0]))
                con.commit()
                # Row 3 column 4 SRI_TO GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'onDialogTimeoutafterSRIRequest'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_3d');".format(r2, result1[0]))
                con.commit()

                # Row 4 column 1 FWSM timeout breakdown 1 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_4a');".format(r2, result1[0]))
                con.commit()
                # Row 4 column 1 FWSM timeout breakdown 1 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_4a';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()


                # Row 4 column 2 FWSM timeout breakdown 2 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_4b');".format(r2, result1[0]))
                con.commit()
                 # Row 4 column 2 FWSM timeout breakdown 1 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_4b';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 4 column 3 FWSM timeout breakdown 3 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_4c');".format(r2, result1[0]))
                con.commit()
                # Row 4 column 3 FWSM timeout breakdown 1 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_4c';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 4 column 4 FWSM timeout breakdown 4 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_4d');".format(r2, result1[0]))
                con.commit()
                # Row 4 column 4 FWSM timeout breakdown 1 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_4d';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 5 column 1 FWSM timeout breakdown 1 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_5a');".format(r2, result1[0]))
                con.commit()
                # Row 5 column 1 FWSM timeout breakdown 1 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_5a';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 5 column 2 FWSM timeout breakdown 2 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_5b');".format(r2, result1[0]))
                con.commit()
                # Row 5 column 2 FWSM timeout breakdown 2 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_5b';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 5 column 3 FWSM timeout breakdown 3 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_5c');".format(r2, result1[0]))
                con.commit()
                # Row 5 column 3 FWSM timeout breakdown 3 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_5c';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 5 column 4 FWSM timeout breakdown 4 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_5d');".format(r2, result1[0]))
                con.commit()
                # Row 5 column 4 FWSM timeout breakdown 4 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52501%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_5d';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 6 column 1 FWSM timeout breakdown 1 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_6a');".format(r2, result1[0]))
                con.commit()
                # Row 6 column 1 FWSM timeout breakdown 1 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_6a';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 6 column 2 FWSM timeout breakdown 2 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_6b');".format(r2, result1[0]))
                con.commit()
                # Row 6 column 2 FWSM timeout breakdown 2 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_6b';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 6 column 3 FWSM timeout breakdown 3 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_6c');".format(r2, result1[0]))
                con.commit()
                # Row 6 column 3 FWSM timeout breakdown 3 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_6c';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()
                
                # Row 6 column 4 FWSM timeout breakdown 4 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_6d');".format(r2, result1[0]))
                con.commit()
                # Row 6 column 4 FWSM timeout breakdown 4 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_6d';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 7 column 1 FWSM timeout breakdown 1 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_7a');".format(r2, result1[0]))
                con.commit()
                # Row 7 column 1 FWSM timeout breakdown 1 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_7a';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 7 column 2 FWSM timeout breakdown 2 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_7b');".format(r2, result1[0]))
                con.commit()
                # Row 7 column 2 FWSM timeout breakdown 2 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_7b';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 7 column 3 FWSM timeout breakdown 3 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_7c');".format(r2, result1[0]))
                con.commit()
                # Row 7 column 3 FWSM timeout breakdown 3 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_7c';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 7 column 4 FWSM timeout breakdown 4 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_7d');".format(r2, result1[0]))
                con.commit()
                # Row 7 column 3 FWSM timeout breakdown 3 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52503%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_7d';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 8 column 1 FWSM timeout breakdown 1 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_8a');".format(r2, result1[0]))
                con.commit()
                # Row 8 column 1 FWSM timeout breakdown 1 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_8a';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 8 column 2 FWSM timeout breakdown 2 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_8b');".format(r2, result1[0]))
                con.commit()
                # Row 8 column 2 FWSM timeout breakdown 2 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_8b';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 8 column 3 FWSM timeout breakdown 3 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_8c');".format(r2, result1[0]))
                con.commit()
                # Row 8 column 3 FWSM timeout breakdown 3 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_8c';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 8 column 4 FWSM timeout breakdown 4 GT 3197015001050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_8d');".format(r2, result1[0]))
                con.commit()
                # Row 8 column 4 FWSM timeout breakdown 4 GT 3197015001050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '3197015001050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_8d';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 9 column 1 FWSM timeout breakdown 1 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_9a');".format(r2, result1[0]))
                con.commit()
                # Row 9 column 1 FWSM timeout breakdown 1 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('tata01,', 'tata02,', 'tata03,', 'tata11,', 'tata12,', 'tata13,', 'tatac01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_9a';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 9 column 2 FWSM timeout breakdown 2 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_9b');".format(r2, result1[0]))
                con.commit()
                # Row 9 column 2 FWSM timeout breakdown 2 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('ibasis01,', 'ibasis02,', 'ibasis03,', 'ibasis11,', 'ibasis12,', 'ibasis13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_9b';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 9 column 3 FWSM timeout breakdown 3 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_9c');".format(r2, result1[0]))
                con.commit()
                # Row 9 column 3 FWSM timeout breakdown 3 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('comfone01,', 'comfone02,', 'comfone03,', 'comfone11,', 'comfone12,', 'comfone13,', 'comfonec01,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_9c';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Row 9 column 4 FWSM timeout breakdown 4 GT 61491500050
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'onDialogTimeoutafterMtForwardSMRequest' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("insert into crm_row1_1 (time, total, success, failed, user_id) VALUES ('{}', '{}', '', '', 'sg_9d');".format(r2, result1[0]))
                con.commit()
                # Row 9 column 4 FWSM timeout breakdown 4 GT 61491500050 ErrorsmDeliveryFailureafterMtForwardSMRequest
                cur.execute("SELECT count(*) FROM crm_cdrprocess where time like '{}%' and msisdn like '{}%' and gt = '61491500050,' and networkid IN ('bics01,', 'bics02,', 'bics03,', 'bics11,', 'bics12,', 'bics13,') and error_msg = 'ErrorsmDeliveryFailureafterMtForwardSMRequest:' and imsi like '52505%'".format(r2, ccsg))  # Query total
                result1 = cur.fetchone()
                cur.execute("UPDATE crm_row1_1 SET failed = '{}' WHERE time like '{}%' and user_id = 'sg_9d';".format(result1[0], r2))  # A bit of dirty solution. It error was added later and updated into the failed field.
                con.commit()

                # Insert into crm_cdrprocess(date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) values('', '', '6511111111', 'failed,', '3197015001050,', 'tata01,', '', '', '5250111111111', 'onDialogTimeoutafterMtForwardSMRequest')

            cur.close()


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
                        # print (p)

                        # run sc



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
                # Route 3 comfonec01 6994 over primary
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9111111111,', 'success,', '3197015001052,', 'comfonec01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9111111111,', 'failed,', '3197015001052,', 'comfonec01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9111111111,', 'failed,', '3197015001052,', 'comfonec01', 'smsc-2-eu4,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9111111111,', 'temp_failed,', '3197015001052,', 'comfonec01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9111111111,', 'partial,', '3197015001052,', 'comfonec01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))

                # Route 3 comfonec01 6994 over secondary
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9122222222,', 'success,', '3197015001052,', 'comfonec01', 'smsc-2-eu1,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9122222222,', 'failed,', '3197015001052,', 'comfonec01', 'smsc-2-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9122222222,', 'failed,', '3197015001052,', 'comfonec01', 'smsc-2-eu1,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9122222222,', 'temp_failed,', '3197015001052,', 'comfonec01', 'smsc-2-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9122222222,', 'partial,', '3197015001052,', 'comfonec01', 'smsc-2-eu1,', 'vlr', 'imsi', 'null');".format(r2))

                # Route 1 syniversec01 6995 over primary
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9133333333,', 'success,', '3197015001050,', 'syniversec01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9133333333,', 'failed,', '3197015001050,', 'syniversec01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9133333333,', 'failed,', '3197015001050,', 'syniversec01', 'smsc-2-eu4,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9133333333,', 'temp_failed,', '3197015001050,', 'syniversec01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9133333333,', 'partial,', '3197015001050,', 'syniversec01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))

                # Route 1 syniversec01 6995 over primary
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9144444444,', 'success,', '3197015001050,', 'syniversec01', 'smsc-2-eu1,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9144444444,', 'failed,', '3197015001050,', 'syniversec01', 'smsc-2-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9144444444,', 'failed,', '3197015001050,', 'syniversec01', 'smsc-2-eu1,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9144444444,', 'temp_failed,', '3197015001050,', 'syniversec01', 'smsc-2-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9144444444,', 'partial,', '3197015001050,', 'syniversec01', 'smsc-2-eu1,', 'vlr', 'imsi', 'null');".format(r2))


                # Route 2 Syniverse 6908 over all 4 SMSC
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'success,', '3197015001051,', 'syniverse01', 'smsc-1-eu1,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'failed,', '3197015001051,', 'syniverse01', 'smsc-1-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'failed,', '3197015001051,', 'syniverse01', 'smsc-1-eu1,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'temp_failed,', '3197015001051,', 'syniverse01', 'smsc-1-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'partial,', '3197015001051,', 'syniverse01', 'smsc-1-eu1,', 'vlr', 'imsi', 'null');".format(r2))


                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'success,', '3197015001051,', 'syniverse01', 'smsc-2-eu1,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'failed,', '3197015001051,', 'syniverse01', 'smsc-2-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'failed,', '3197015001051,', 'syniverse01', 'smsc-2-eu1,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'temp_failed,', '3197015001051,', 'syniverse01', 'smsc-2-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'partial,', '3197015001051,', 'syniverse01', 'smsc-2-eu1,', 'vlr', 'imsi', 'null');".format(r2))

                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'success,', '3197015001051,', 'syniverse01', 'smsc-1-eu4,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'failed,', '3197015001051,', 'syniverse01', 'smsc-1-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'failed,', '3197015001051,', 'syniverse01', 'smsc-1-eu4,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'temp_failed,', '3197015001051,', 'syniverse01', 'smsc-1-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'partial,', '3197015001051,', 'syniverse01', 'smsc-1-eu4,', 'vlr', 'imsi', 'null');".format(r2))


                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'success,', '3197015001051,', 'syniverse01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'failed,', '3197015001051,', 'syniverse01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'failed,', '3197015001051,', 'syniverse01', 'smsc-2-eu4,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'temp_failed,', '3197015001051,', 'syniverse01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9155555555,', 'partial,', '3197015001051,', 'syniverse01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))


                # Route 4 Syniverse 6909 over all 4 SMSC
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'success,', '3197015001053,', 'comfone01', 'smsc-1-eu1,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'failed,', '3197015001053,', 'comfone01', 'smsc-1-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'failed,', '3197015001053,', 'comfone01', 'smsc-1-eu1,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'temp_failed,', '3197015001053,', 'comfone01', 'smsc-1-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'partial,', '3197015001053,', 'comfone01', 'smsc-1-eu1,', 'vlr', 'imsi', 'null');".format(r2))

                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'success,', '3197015001053,', 'comfone01', 'smsc-2-eu1,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'failed,', '3197015001053,', 'comfone01', 'smsc-2-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'failed,', '3197015001053,', 'comfone01', 'smsc-2-eu1,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'temp_failed,', '3197015001053,', 'comfone01', 'smsc-2-eu1,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'partial,', '3197015001053,', 'comfone01', 'smsc-2-eu1,', 'vlr', 'imsi', 'null');".format(r2))

                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'success,', '3197015001053,', 'comfone01', 'smsc-1-eu4,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'failed,', '3197015001053,', 'comfone01', 'smsc-1-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'failed,', '3197015001053,', 'comfone01', 'smsc-1-eu4,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'temp_failed,', '3197015001053,', 'comfone01', 'smsc-1-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'partial,', '3197015001053,', 'comfone01', 'smsc-1-eu4,', 'vlr', 'imsi', 'null');".format(r2))

                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'success,', '3197015001053,', 'comfone01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'failed,', '3197015001053,', 'comfone01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'failed,', '3197015001053,', 'comfone01', 'smsc-2-eu4,', 'vlr', 'imsi', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'temp_failed,', '3197015001053,', 'comfone01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '9166666666,', 'partial,', '3197015001053,', 'comfone01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))

                ## insert test data for new SG
                # cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6577777777,', 'success,', '3197015001050,', 'comfone01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6577777777,', 'failed,', '3197015001050,', 'tata01,', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6577777777,', 'failed,', '3197015001050,', 'ibasis01', 'smsc-2-eu4,', 'vlr', '52503', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6577777777,', 'failed,', '3197015001050,', 'bics01', 'smsc-2-eu4,', 'vlr', '52503', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6577777777,', 'temp_failed,', '3197015001050,', 'comfone01', 'smsc-2-eu4,', 'vlr', '52505', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                # cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6577777777,', 'temp_failed,', '3197015001050,', 'comfone01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                # cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6577777777,', 'partial,', '3197015001050,', 'tatac01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))
                #
                # cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6588888888,', 'success,', '61491500050,', 'comfone01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))
                # cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6588888888,', 'failed,', '61491500050,', 'tata01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                # cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6588888888,', 'failed,', '61491500050,', 'ibasis01', 'smsc-2-eu4,', 'vlr', '52501', 'ErrorsmDeliveryFailureafterMtForwardSMRequest:');".format(r2))
                # cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6588888888,', 'temp_failed,', '61491500050,', 'comfone01', 'smsc-2-eu4,', 'vlr', '52503', 'onDialogTimeoutafterMtForwardSMRequest');".format(r2))
                # cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6588888888,', 'temp_failed,', '61491500050,', 'comfone01', 'smsc-2-eu4,', 'vlr', 'imsi', 'onDialogTimeoutafterSRIRequest');".format(r2))
                # cur.execute("insert into crm_cdrprocess (date, time, msisdn, status, gt, networkid, system, msc, imsi, error_msg) VALUES ('date', '{}', '6588888888,', 'partial,', '61491500050,', 'tatac01', 'smsc-2-eu4,', 'vlr', 'imsi', 'null');".format(r2))

                con.commit()
            cur.close()

    # This part is for FB
    row1_1a = row1_1.objects.filter(user_id='1a').order_by('time')
    row1_1b = row1_1.objects.filter(user_id='1b').order_by('time')
    row1_1c = row1_1.objects.filter(user_id='1c').order_by('time')
    row1_1d = row1_1.objects.filter(user_id='1d').order_by('time')
    row1_1e = row1_1.objects.filter(user_id='1e').order_by('time')

    row1_2a = row1_1.objects.filter(user_id='2a').order_by('time')
    row1_2b = row1_1.objects.filter(user_id='2b').order_by('time')
    row1_2c = row1_1.objects.filter(user_id='2c').order_by('time')
    row1_2d = row1_1.objects.filter(user_id='2d').order_by('time')
    row1_2e = row1_1.objects.filter(user_id='2e').order_by('time')




    context = {
        'row1_1a': row1_1a,
        'row1_1b': row1_1b,
        'row1_1c': row1_1c,
        'row1_1d': row1_1d,
        'row1_1e': row1_1e,
        'row1_2a': row1_2a,
        'row1_2b': row1_2b,
        'row1_2c': row1_2c,
        'row1_2d': row1_2d,
        'row1_2e': row1_2e,

    }

    return render(request, 'crm/fb.html', context )


def newSG(request):

    # This part is for new version of SG
    row1_sg_1a = row1_1.objects.filter(user_id='sg_1a').order_by('time')
    row1_sg_1b = row1_1.objects.filter(user_id='sg_1b').order_by('time')
    row1_sg_1c = row1_1.objects.filter(user_id='sg_1c').order_by('time')
    row1_sg_1d = row1_1.objects.filter(user_id='sg_1d').order_by('time')
    row1_sg_1e = row1_1.objects.filter(user_id='sg_1e').order_by('time')
    row1_sg_2a = row1_1.objects.filter(user_id='sg_2a').order_by('time')
    row1_sg_2b = row1_1.objects.filter(user_id='sg_2b').order_by('time')
    row1_sg_2c = row1_1.objects.filter(user_id='sg_2c').order_by('time')
    row1_sg_2d = row1_1.objects.filter(user_id='sg_2d').order_by('time')

    row1_sg_3a = row1_1.objects.filter(user_id='sg_3a').order_by('time')
    row1_sg_3b = row1_1.objects.filter(user_id='sg_3b').order_by('time')
    row1_sg_3c = row1_1.objects.filter(user_id='sg_3c').order_by('time')
    row1_sg_3d = row1_1.objects.filter(user_id='sg_3d').order_by('time')

    row1_sg_4a = row1_1.objects.filter(user_id='sg_4a').order_by('time')
    row1_sg_4b = row1_1.objects.filter(user_id='sg_4b').order_by('time')
    row1_sg_4c = row1_1.objects.filter(user_id='sg_4c').order_by('time')
    row1_sg_4d = row1_1.objects.filter(user_id='sg_4d').order_by('time')

    row1_sg_5a = row1_1.objects.filter(user_id='sg_5a').order_by('time')
    row1_sg_5b = row1_1.objects.filter(user_id='sg_5b').order_by('time')
    row1_sg_5c = row1_1.objects.filter(user_id='sg_5c').order_by('time')
    row1_sg_5d = row1_1.objects.filter(user_id='sg_5d').order_by('time')

    row1_sg_6a = row1_1.objects.filter(user_id='sg_6a').order_by('time')
    row1_sg_6b = row1_1.objects.filter(user_id='sg_6b').order_by('time')
    row1_sg_6c = row1_1.objects.filter(user_id='sg_6c').order_by('time')
    row1_sg_6d = row1_1.objects.filter(user_id='sg_6d').order_by('time')

    row1_sg_7a = row1_1.objects.filter(user_id='sg_7a').order_by('time')
    row1_sg_7b = row1_1.objects.filter(user_id='sg_7b').order_by('time')
    row1_sg_7c = row1_1.objects.filter(user_id='sg_7c').order_by('time')
    row1_sg_7d = row1_1.objects.filter(user_id='sg_7d').order_by('time')

    row1_sg_8a = row1_1.objects.filter(user_id='sg_8a').order_by('time')
    row1_sg_8b = row1_1.objects.filter(user_id='sg_8b').order_by('time')
    row1_sg_8c = row1_1.objects.filter(user_id='sg_8c').order_by('time')
    row1_sg_8d = row1_1.objects.filter(user_id='sg_8d').order_by('time')

    row1_sg_9a = row1_1.objects.filter(user_id='sg_9a').order_by('time')
    row1_sg_9b = row1_1.objects.filter(user_id='sg_9b').order_by('time')
    row1_sg_9c = row1_1.objects.filter(user_id='sg_9c').order_by('time')
    row1_sg_9d = row1_1.objects.filter(user_id='sg_9d').order_by('time')


    context = {
        'row1_sg_1a': row1_sg_1a,
        'row1_sg_1b': row1_sg_1b,
        'row1_sg_1c': row1_sg_1c,
        'row1_sg_1d': row1_sg_1d,
        'row1_sg_1e': row1_sg_1e,
        'row1_sg_2a': row1_sg_2a,
        'row1_sg_2b': row1_sg_2b,
        'row1_sg_2c': row1_sg_2c,
        'row1_sg_2d': row1_sg_2d,
        'row1_sg_3a': row1_sg_3a,
        'row1_sg_3b': row1_sg_3b,
        'row1_sg_3c': row1_sg_3c,
        'row1_sg_3d': row1_sg_3d,
        'row1_sg_4a': row1_sg_4a,
        'row1_sg_4b': row1_sg_4b,
        'row1_sg_4c': row1_sg_4c,
        'row1_sg_4d': row1_sg_4d,
        'row1_sg_5a': row1_sg_5a,
        'row1_sg_5b': row1_sg_5b,
        'row1_sg_5c': row1_sg_5c,
        'row1_sg_5d': row1_sg_5d,
        'row1_sg_6a': row1_sg_6a,
        'row1_sg_6b': row1_sg_6b,
        'row1_sg_6c': row1_sg_6c,
        'row1_sg_6d': row1_sg_6d,
        'row1_sg_7a': row1_sg_7a,
        'row1_sg_7b': row1_sg_7b,
        'row1_sg_7c': row1_sg_7c,
        'row1_sg_7d': row1_sg_7d,
        'row1_sg_8a': row1_sg_8a,
        'row1_sg_8b': row1_sg_8b,
        'row1_sg_8c': row1_sg_8c,
        'row1_sg_8d': row1_sg_8d,
        'row1_sg_9a': row1_sg_9a,
        'row1_sg_9b': row1_sg_9b,
        'row1_sg_9c': row1_sg_9c,
        'row1_sg_9d': row1_sg_9d,
    }

    return render(request, 'crm/newSG.html', context)





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
