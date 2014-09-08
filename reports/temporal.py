#!/usr/bin/python

#each memdb module should provide a number of functions that will be called arbitrarily by the generator
#parse_event and get_report

from collections import OrderedDict
from PIL import Image

class memdb_module:
	__name__ = "temporal"

	def __init__(self, helper):
		self.helper = helper #helper is report_helper.py, helps to create proper paths etc

		self.target_stack = helper.args.func.split("::")
		self.target_stack_matched = []

		self.func_addresses = []  #list containing lists of addresses for each function invocation
		self.global_order = {} #track the global order of all seen addresses

		self.address_list = [] #list of all addresses the current function has touched
		self.address_count = OrderedDict() #count of all the times an address has been touched

	def parse_event(self, event):
		if len(self.target_stack) > 0 and event['event'] == 'function-begin' and event['name'] == self.target_stack[0]:
			#pop from target stack and push to matched stack
			self.target_stack_matched.append(self.target_stack.pop(0))

		if len(self.target_stack_matched) > 0 and event['event'] == 'function-end' and event['name'] == self.target_stack_matched[-1]:
			if len(self.target_stack) == 0:
				#append current set of addresses to the list
				self.func_addresses.append(self.address_count) 

				#update the global order
				for addr in self.address_count:
					if addr not in self.global_order:
						pos = len(self.global_order);
						self.global_order[addr] = pos;
				#end record tr

				#reset address list
				self.address_list = []
				self.address_count = OrderedDict()

			#move the function from one stack to the other
			self.target_stack.insert(0, self.target_stack_matched.pop(-1))

		if len(self.target_stack) == 0:
			if event["event"] == "memory-access":
				#addr = mem_access['address']
				addr = event['region-base'] #best to record region base instead (allocation objects)
				
				self.address_list.append( addr )

				#append to address map for the current invocation
				if addr in self.address_count:
					self.address_count[ addr ]['count'] = self.address_count[ addr ]['count'] + 1
				else:
					event['count'] = 1
					self.address_count[ addr ] = event

	def write_tr_image(self, filename):
		#if args.keysort:
			#tr_list = [ tr for (k,tr) in sorted(zip(key_list, tr_list)) ]
			#tr_list = sorted()

		width = len(self.global_order)
		height = len(self.func_addresses)
		
		print "Generating %d x %d temporal locality image" % (width,height)
		img = Image.new("RGB", (width, height), color=(255,255,255)) #for first parameter (mode), see: http://pillow.readthedocs.org/en/latest/handbook/concepts.html
		imga = img.load()

		count = 0
		for tr in self.func_addresses:
			#print "--"
			for (addr,access) in tr.items():
				x = self.global_order[addr]; #width
				y = count

				#print (x,y)
				if access['type'] == "read":
					imga[x,y] = (0,0,0) # set to black
				else:
					imga[x,y] = (255,0,0) # set to black

			count = count + 1

		img.save(filename)

	def write_spatial_image(self, filename):
		#writes an image depicting the spatial locality of each function call 

		#create a mapping between addresses and columns in the image
		columns = map (lambda x: int(x, 0), self.global_order.keys())
		columns = map (lambda x: x / 64, columns) #turn address accesses into cache line accesses, for readability
		offset = min(columns)
		columns = map(lambda x: x-offset, columns)
		addr_to_columns = {key: value for (key,value) in zip(self.global_order.keys(), columns)}

		#create image
		width = max(columns)+1
		height = len(self.func_addresses)
		print "Generating %d x %d spatial locality image" % (width,height)
		img = Image.new("RGB", (width, height), color=(255,255,255)) #for first parameter (mode), see: http://pillow.readthedocs.org/en/latest/handbook/concepts.html
		imga = img.load()

		#output image
		count = 0
		for tr in self.func_addresses:
			#print "--"
			for (addr,access) in tr.items():
				x = addr_to_columns[addr]; #width
				y = count

				if access['type'] == "read":
					imga[x,y] = (0,0,0) # set to black
				else:
					imga[x,y] = (255,0,0) # set to black

			count = count + 1

		img.save(filename)

	def get_report(self):
		#generate report and return details for the main report file
		self.write_tr_image(self.helper.get_path("TR.png"))
		self.write_spatial_image(self.helper.get_path("SL.png"))

		#sort the list by keys
		print "Sorting functions by addresses"
		self.func_addresses.sort(key=lambda x: ''.join(x.keys()))

		self.write_tr_image(self.helper.get_path("TR-sorted.png"))
		self.write_spatial_image(self.helper.get_path("SL-sorted.png"))

		template = self.helper.env.get_template("temporal.html")
		open(self.helper.get_path("temporal.html"), "w").write(template.render())

		template = self.helper.env.get_template("spatial.html")
		open(self.helper.get_path("spatial.html"), "w").write(template.render())

		return [{"url" : "temporal.html", "title": "Temporal Locality"}, {"url" : "spatial.html", "title": "Spatial Locality"}]

