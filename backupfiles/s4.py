# s4.py
#!/usr/bin/python
import os

os.system('ssh smsc-1-eu4-prod python /home/kennyC/sms/cdrhour.py -s 10-30 1001 >> /tmp/mylog.txt 2>&1')
