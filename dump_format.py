#!/usr/bin/python
#dump the format for each event type based on a JSON trace file
# basically we define the format based on how we use it :D

import json, sys

f = sys.stdin

events = dict()

for line in f:
	event = json.loads(line)

	if event['event'] not in events:
		events[event['event']] = event

for (k,v) in events.iteritems():
	print json.dumps(v)