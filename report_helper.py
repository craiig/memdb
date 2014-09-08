#class to help reports look up command line args, create files, etc

import os

class report_helper:
	def __init__(self, args):
		self.args = args
		self.output_directory = args.o

	def get_path(self, path):
		#return proper path relative to the output output_directory
		p = os.path.join(self.output_directory, path)
		return p