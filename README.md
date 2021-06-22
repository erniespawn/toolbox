## Prerequisites:
- python3.8
- Install Django 3.1.2

### Python Virtual Environment.
- Create new virtualenv -- > python3.8 -m venv env3.8
- Change into DIR -- > cd env3.8
- Activate env -- > source bin/active



### Install Django 

|    Description    | Command                |
| :-----------: | ------------------        |
|  Install Django  | pip install Django==3.1.2         |
|  Create project   | django-admin startproject mysite           |
|  Change directory in mysite | cd mysite        |
|  Create an app | python manage.py startapp crm        |


### Configure


## Info for insert records into db with Django shell 
```
python manage.py shell
from crm.models import CdrProcess
from crm.models import row1_1

row1_1.objects.all().count()
```

### Insert for SRI
```
q = CdrProcess(time="19:00:00.720,", date='2021-04-04', msisdn='65819018040,', status='temp_failed,', system='smsc-2-eu4,', error_msg='onDialogTimeoutafterSRIRequest', networkid='1001,', gt='3197015001050,')
q.save()
```

### Insert for FWSM
```
x = CdrProcess(time="19:32:00.720,", date='2021-04-04', msisdn='65819018040,', status='temp_failed,', system='smsc-2-eu4,', error_msg='onDialogTimeoutafterMtForwardSMRequest', networkid='1003,', gt='3197015001050,', imsi='52503')
x.save()
```

### Using sqlite3
``` 
Make sure your enviruoment is activated with  'source ../bin/activate'
To start it `sqlite3 db.sqlite3`

.schema
select * from crm_cdrprocess limit 3;
select * from crm_row1_1 limit 3;

```

### Using python smpplib
``` 

```



### Login to DB
```
kennyC@dev-instance-eu1-prod:~$ cd django/
source bin/activate
cd mysite/
sqlite3 db.sqlite3

```
