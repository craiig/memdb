#!/usr/bin/python

import sys, json, re, argparse

parser = argparse.ArgumentParser(description='Print out statistics of memory accesses based on a trace')
parser.add_argument('-f', metavar="trace file", help="input filename, otherwise stdin is used", nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('-d', help="debug the parser", action="store_true", default=False)
arg_source = sys.argv[1:]
args = parser.parse_args(arg_source)

for line in args.f:
	line = line.strip()

	valid = re.match("^(function-begin|function-end|allocation-free|allocation|memory-access|region-free)\s*(.*)$", line)
	if valid:
		if(args.d):
			#print "event match:" + valid.group(1)
			#print valid.group(2)
			pass

		event = valid.group(1)

		output = dict()
		output['event'] = event

		if event == 'function-begin' or event == 'function-end':
			output['name'] = line.split(":")[1]
		elif event == 'memory-access'  or event == "allocation ":
			remainder = valid.group(2)

			#build a dictionary out of the values on this line and append it to the output
			#todo; this assumes the attributes passed from the trace are the ones we want to use
			#      which will probably not be true in the long run...
			output.update({ k:v for [k,v] in map(lambda x: x.split(':'), remainder.split(" ")) } )
		else:
			output['remainder'] = valid.group(2)

		print json.dumps(output)

		pass
	elif args.d:
		print "non matching line: %s" % (line)
