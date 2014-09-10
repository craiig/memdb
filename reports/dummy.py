#!/usr/bin/python

#each memdb module should provide a number of functions that will be called arbitrarily by the generator
#this file is an example of all the things a module can do

from collections import OrderedDict
from PIL import Image

class memdb_module:
	__name__ = "dummy"

	def __init__(self, helper):
		#called
		pass

	def parse_all_events(self, event):
		#called on all events
		pass

	def enter_target_func(self, event):
		#called when the target function is entered
		pass

	def exit_target_func(self, event):
		#called when the target function is left
		pass

	def parse_event(self, event):
		pass

	def get_report(self):
		pass
