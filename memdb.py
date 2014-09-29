#!/usr/local/bin/python

# this tool drives the generation of a report, based on the scripts included in reports/

import argparse, sys, json, os, gzip
import pkgutil, inspect, reports
import report_helper
from jinja2 import Environment, FileSystemLoader

#parse input
parser = argparse.ArgumentParser(description='Generate a report based on JSON trace file')
parser.add_argument('-f', metavar="trace file in JSON format", help="input filename, otherwise stdin is used", nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('-o', metavar="output directory", help="output directory")
parser.add_argument('-func', help="function of interest", type=str)
#parser.add_argument('-d', help="debug the parser", action="store_true", default=False)
arg_source = sys.argv[1:]
args = parser.parse_args(arg_source)

#test for GZIP'd file input
#gzip won't tell you if it's a gzipped file until you start to read
gzip_file = gzip.GzipFile(fileobj=args.f)
try:
	gzip_file.read(1)
	args.f = gzip_file
except IOError as e:
	pass
args.f.seek(0)

#check to see if a function was specified
if not args.func:
	print "Function of interest not specified, please choose one below and add --func <function>" 
	functions = dict()
	for line in args.f:
		event = json.loads(line)
		if event['event'] == 'function-begin':
			if event['name'] not in functions:
				functions[event['name']] = 1
			else:
				functions[event['name']] = functions[event['name']] + 1

	print "# calls\tfunction name"
	for x in sorted(functions.iteritems(), key=lambda x: x[1], reverse=True):
		print "%s\t%s" % (x[1], x[0])
	sys.exit()

#setup the output directory
if not args.o:
	print "Error: no output directory provided"
	parser.print_help()
	sys.exit()

output_directory = args.o
if os.path.exists(output_directory):
	print "Error: output directory '%s' already exists. Won't overwrite for safety." % (args.o)
	sys.exit()

os.mkdir(output_directory)

#setup report helper
helper = report_helper.report_helper(args)

#iterate over all modules, importing them and calling the report setup functions
#code borrowed from http://stackoverflow.com/questions/1707709/list-all-the-modules-that-are-part-of-a-python-package
reports_to_run = []
prefix = reports.__name__ + "."
for importer, modname, ispkg in pkgutil.iter_modules(reports.__path__, prefix):
    #print "Found report %s (is a package: %s)" % (modname, ispkg)
    print "Importing report %s" % (modname)
    m = __import__(modname, fromlist="dummy")
    #instantiate the class inside the module, makes it easier to maintain parse state inside each report
    #passing output directory and args 
    reports_to_run.append( m.memdb_module(helper) ) 

#parse the input file, paying attention to only call the modules in the function of interest
#we use a couple stacks here to figure out when we're inside the function of interest
target_stack = helper.args.func.split("::")
target_stack_matched = []
print "Parsing input"
for line in args.f:
	event = json.loads(line)

	for r in reports_to_run:
		r.parse_all_events(event)

	if len(target_stack) > 0 and event['event'] == 'function-begin' and event['name'] == target_stack[0]:
			#pop from target stack and push to matched stack
			target_stack_matched.append(target_stack.pop(0))
			if len(target_stack) == 0:
				#begun the function
				for r in reports_to_run:
					r.enter_target_func(event)

	if len(target_stack_matched) > 0 and event['event'] == 'function-end' and event['name'] == target_stack_matched[-1]:
		if len(target_stack) == 0:
			#leaving the function
			for r in reports_to_run:
				r.exit_target_func(event)

		#move the function from one stack to the other
		target_stack.insert(0, target_stack_matched.pop(-1))

	if len(target_stack) == 0:
		for r in reports_to_run:
			r.parse_event(event)

#setup jinja2 environment
template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
helper.env = Environment(loader=FileSystemLoader( template_dir ) ) 
helper.env.globals['reports'] = []

#generate the reports
for r in reports_to_run:
	#test = __import__("reports." + r)
	#print dir(r)
	info = r.get_report()
	if info:
		helper.env.globals['reports'].extend(info)

#render index template to a file
index_template = helper.env.get_template("index.html")
f = open(helper.get_path("index.html"), "w")
f.write(index_template.render())
f.close()