#!/usr/bin/python

# in D3 objects are drawn on an svg canvas using x,y points
# we just need to draw the x,y points

# note that we can supply the x,y points as literals and use a transform to change their offsets later

import json

class memdb_module:
	__name__ = "d3spatial"

	def __init__(self, helper):
		self.helper = helper
		self.cur_x_min = None
		self.cur_x_max = None
		self.func_count = 0

		#self.target_stack = helper.args.func.split("::")
		#self.target_stack_matched = []

		self.json_file = open(helper.get_path("d3spatial-points.json"), "w")
		self.json_file.write("var datapoints = [\n")
		pass

	def parse_all_events(self, event):
		pass

	def enter_target_func(self, event):
		pass

	def exit_target_func(self, event):
		self.func_count = self.func_count + 1

	def parse_event(self, event): #only called inside the target function
		#{"function": "_ZN14brandonpelfrey8QuadtreeC1ERK4Vec2S3_", 
	#		"region-base": "0xcb3010", 
	#		"pc": "0x40231b", 
	#		"region-size": "80", 
	#		"address": "0xcb3010", 
	#		"type": "write", 
	#		"event": "memory-access", 
	#		"region-tag": "1"
	#	}

		if event['event'] == "memory-access":
			int_addr = float(int(event['region-base'], 0)) / 64
			if self.cur_x_min:
				self.cur_x_min = min(self.cur_x_min, int_addr)
			else:
				self.cur_x_min = int_addr

			if self.cur_x_max:
				self.cur_x_max = max(self.cur_x_max, int_addr + float(event['region-size']) /64 )
			else:
				self.cur_x_max = int_addr + float(event['region-size']) / 64

			#if int_addr not in self.regions:
			#	self.regions[int_addr] = len(self.regions)
			#
			#int_addr = self.regions[int_addr]
			#self.cur_x_min = 0;
			#self.cur_x_max = int_addr;

			point = dict()
			point['x'] = int_addr
			point['y'] = self.func_count
			point['width'] = float(event['region-size']) / 64
			point['type'] = event['type']
			point['full_info'] = event

			self.json_file.write( json.dumps(point) )
			self.json_file.write(",\n")

		pass

	def get_report(self):
		self.json_file.write("];\n")
		self.json_file.write("var datapoints_x_min = %d;\n" % self.cur_x_min)
		self.json_file.write("var datapoints_x_max = %d;\n" % self.cur_x_max)
		self.json_file.write("var datapoints_y_max = %d;\n" % self.func_count)

		template = self.helper.env.get_template("d3spatial.html")
		open(self.helper.get_path("d3spatial.html"), "w").write(template.render())

		return [{"url" : "d3spatial.html", "title": "Spatial Locality (D3)"}]