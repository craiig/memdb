#!/usr/local/bin/python
import gzip, sys, json

#f = open("../test/wiredtiger/wt-ldb-readrand2.json.gz")
f = open("../test/wiredtiger/ldb-readrandom-24t.json.gz")
gzip_file = gzip.GzipFile(fileobj=f)

#print dir(sys)
#print dir(gzip_file)
#print gzip_file.__sizeof__()
#sys.exit()

#allocs = dict()
count = 0
for line in gzip_file:
	#if count == 10:
	#	sys.exit()
	#else:
	#	count = count + 1

	e = json.loads(line)
	if e['event'] == "allocation":
		#if e['alloc-base'] in allocs:
		#	print "free " + json.dumps(e)
		#else:
		#allocs[e['alloc-base']] = 1
		#print json.dumps(e)
		print line.strip()
	if e['event'] == "memory-access":
		if e['alloc-location'] != '<unknown>':
			#print json.dumps(e)
			print gzip_file.fileobj.tell()
			print line
			sys.exit()
	else:
		pass