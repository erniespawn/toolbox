#!/usr/bin/python

# This file is running on the SMSC under directory /home/kennyC/sms

import gzip
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("-s")
#parse.add_argument('msisdn')
parse.add_argument('route')
args = parse.parse_args()
# print argument of -s


class Views(object):
	def __init__(self, msisdn, status, networkid, date, gt, system):
		self.msisdn = msisdn
		self.status = status
		self.networkid = networkid
		self.date = date
		self.gt = gt
		self.system = system

	def show(self):
		print "{}, {}, {}, {}, {}, {}".format(self.status, self.msisdn, self.networkid, self.date, self.gt, self.system)

	def report(self):
		if self.networkid == '1001':
                    pass


class Progresor(object):
	def __init__(self):
		self.passer = []
		self.build()

	def build(self):
		#with gzip.open("/home/kennyC/sms/cdr-2021-02-01-01.gz",'rb') as f:
		#with open("/home/kennyC/sms/cdr.log",'rb') as f:
		with open("/var/log/restcomm/cdr.log",'rb') as f:
    		    line_file1 = f.readlines()
    		    for line in line_file1:
		        list = []
		        list = " ".join(line.split())
		        st = list.split(',')
		        try:
			    if len(st) == 19:
			        if st[11] != 'success_esme':
		    	               self.passer.append(Views(st[11], st[8], st[3], st[0], st[7], 'smsc-2-eu4'))
		        except:
                            pass

        def show(self):
            for c in self.passer:
                c.show()



parser = Progresor()
parser.show()


