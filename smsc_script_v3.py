#!/usr/bin/python

# This file is running on the SMSC under directory /home/kennyC/sms

import gzip
import argparse
import datetime
import datetime
from datetime import datetime, timedelta, date

parse = argparse.ArgumentParser()
parse.add_argument("-s")
#parse.add_argument('msisdn')
parse.add_argument('route')
args = parse.parse_args()
# print argument of -s


class Views(object):
	def __init__(self, msisdn, status, networkid, date, gt, system, msc, imsi, error_msg):
		self.msisdn = msisdn
		self.status = status
		self.networkid = networkid
		self.date = date
		self.gt = gt
		self.system = system
		self.msc = msc
		self.imsi = imsi
		self.error_msg = error_msg

	def show(self):
		print "{}, {}, {}, {}, {}, {}, {}, {}, {}".format(self.status, self.msisdn, self.networkid, self.date, self.gt, self.system, self.msc, self.imsi, self.error_msg)

	def report(self):
		if self.networkid == '1001':
			pass


class Runner(object):
	def __init__(self):
		self.passer = []
		self.build()

	def build(self):
		if args.s == '0':
			with open("/var/log/restcomm/cdr.log",'rb') as f:
					line_file1 = f.readlines()
					for line in line_file1:
						list = []
						list = " ".join(line.split())
						st = list.split(',')
						try:
							
							if len(st) == 19:
								if st[11] != 'success_esme':
									if st[18] == '':
										self.passer.append(Views(st[11], st[8], st[3], st[0], st[7], 'smsc-2-eu4', st[14], st[15], 'null'))
									else:
										self.passer.append(Views(st[11], st[8], st[3], st[0], st[7], 'smsc-2-eu4', st[14], st[15], st[18].replace(" ", "")))
											
						except:
							pass

		elif args.s == 'examplefile':
					
			with gzip.open("/home/kennyC/sms/cdr-2021-02-01-08.gz",'rb') as f:
					line_file1 = f.readlines()
					for line in line_file1:
						list = []
						list = " ".join(line.split())
						st = list.split(',')
						try:
							
							if len(st) == 19:
								if st[11] != 'success_esme':
									if st[18] == '':
										pass
										self.passer.append(Views(st[11], st[8], st[3], st[0], st[7], 'smsc-2-eu4', st[14], st[15], 'null'))  #This only adds the success and partial
									else:
										if st[3] == '0':
											pass
										else:
											self.passer.append(Views(st[11], st[8], st[3], st[0], st[7], 'smsc-2-eu4', st[14], st[15], st[18].replace(" ", ""))) #This only adds the failed and temp_failed

						except:
							pass

		elif args.s == '-1':
			min_hour = datetime.today() - timedelta(hours=1, minutes=0) # Get time and extract 1 hour of it
			g_hour = min_hour.strftime('%H') # Get time and only get the hour 

			g_date = datetime.now().strftime('%m-%d') # Get month and day

			with gzip.open("/var/log/restcomm/cdr-2021-{}-{}.gz".format(g_date, g_hour),'rb') as f:
				line_file1 = f.readlines()
				for line in line_file1:
						list = []
						list = " ".join(line.split())
						st = list.split(',')
						try:
							
							if len(st) == 19:
								if st[11] != 'success_esme':
									if st[18] == '':
										self.passer.append(Views(st[11], st[8], st[3], st[0], st[7], 'smsc-2-eu4', st[14], st[15], 'null'))  #This only adds the success and partial
									else:
										if st[3] == '0':
											pass
										else:
											self.passer.append(Views(st[11], st[8], st[3], st[0], st[7], 'smsc-2-eu4', st[14], st[15], st[18].replace(" ", ""))) #This only adds the failed and temp_failed
						except:
							pass
		
		elif args.s == '-2':
			print ("This is to get 2 previous hours but its not finished yet")


		else:
			pass


	def show(self):
		for c in self.passer:
			c.show()



parser = Runner()
parser.show()

