#!/usr/bin/python

#each memdb module should provide a number of functions that will be called arbitrarily by the generator
#this file is an example of all the things a module can do

from collections import OrderedDict
from PIL import Image

class memdb_module:
	__name__ = "allocation-stats"

	def __init__(self, helper):
		#called
		self.allocations = {}
		pass

	def parse_all_events(self, event):
		#called on all events
		if event['event'] == 'allocation':
			self.allocations[event['alloc-base']] = {
				"read": 0,
				"write": 0,
				"event": event
			}
			#print event

	def enter_target_func(self, event):
		#called when the target function is entered
		pass

	def exit_target_func(self, event):
		#called when the target function is left
		pass

	def parse_event(self, event):
		if event['event'] == 'memory-access':
			if event['region-base'] in self.allocations:
				alloc = self.allocations[event['region-base']]
				
				if event['type'] == 'write':
					alloc['write'] = alloc['write'] + 1

				if event['type'] == 'read':
					alloc['read'] = alloc['read'] + 1
		pass

	def get_report(self):
		unused_allocs = 0
		written_allocs = 0
		read_allocs = 0

		for a in self.allocations.itervalues():
			if a['read'] == 0 and a['write'] == 0:
				unused_allocs =  unused_allocs + 1

			if a['read'] > 0:
				read_allocs = read_allocs + 1

			if a['write'] > 0:
				written_allocs = written_allocs + 1

		#print "total allocs: %d unused allocs: %d read allocs: %d written allocs: %d" % (len(self.allocations), unused_allocs, read_allocs, written_allocs)

		pass
