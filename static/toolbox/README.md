## Prerequisites:
- python3.8
- install mysql client
- Install Django 3.1.2

### Python Virtual Environment.
- Create new virtualenv -- > python3.8 -m venv env3.8
- Change into DIR -- > cd env3.8
- Activate env -- > source bin/active

### Install mysql client and create db
|    Description    | Command                |
| :-----------: | ------------------        |
|  Install mysql client  | python -m pip install django-mysql          |
|  Create password for root  | mysqladmin -u root -p password          |
|  Login to mysql | mysql -u root -p         |
|  Create DB | create database toolbox;       |




### Install Django 

|    Description    | Command                |
| :-----------: | ------------------        |
|  Install Django  | pip install Django==3.1.2         |
|  Create project   | django-admin startproject mysite           |
|  Change directory in mysite | cd mysite        |
|  Create an app | python manage.py startapp crm        |


### Configure

|    Description    | Command                |
| :-----------: | ------------------        |
|  clone this repo  | copy all files to the project.        |
|  Install dependencies   | pip install -r requirements.txt           |
|  mysite/mysite/settings.py | Update credentials for mysql        |
|  Migrate the db | python manage.py migrate        |
|  Start project  | python manage.py runserver        |
|  Reset the db | http://127.0.0.1:8000/crm/reset/       |
|  Press reset| You will see 1 entry in DB       |

- Good luck



## Info for insert records into db with Django shell 
```
python manage.py shell
from crm.models import CdrProcess
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



