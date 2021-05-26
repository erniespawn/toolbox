# nargs_example.py
# cdrhour.py -s 10-30 1001
# https://docs.google.com/spreadsheets/d/1lHRD2gLdQLor-0gHoGvJlTQoWl3HdfJJdXtt86M_Fis/edit#gid=1302559956
import gzip
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("-s")
parse.add_argument('nums', nargs='*')
args = parse.parse_args()
# print argument of -s

counter = 0


a = (args.nums)
for b in a:
	a = b

thishour = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'] 
for x in thishour:
	#print ("cdr-2020-{}-{}.gz".format(args.s, x))

	file = ("/var/log/restcomm/cdr-2020-{}-{}.gz".format(args.s, x))
#file = ("cdr-2020-{}-{}.gz".format(args.s, '01'))

#with gzip.open(args.s, 'rb') as f:
	total_count = 0
	total_success = 0
	tata_total_failed = 0
	tata_total_temp_failed = 0
	tata_total_partial = 0

	with gzip.open(file, 'rb') as f:
		file_content = f.readlines()
		for line in file_content:
			try:
				list = []
				list = " ".join(line.split())
				st = line.split(',')
				#if len(st) == 19:
				if (st[11]) != 'success_esme':
						#print st[3]
						if st[3] == (a):
							total_count = total_count + 1
						if st[3] == (a):
							if st[11] == 'success':
								total_success = total_success + 1
				else:
					pass					
			
			except:
				pass
		#print ('TATA total = ' + str(total_count), ',' 'TATA total success = ' + str(total_success))
		print str(total_count), '\t' + str(total_success)
