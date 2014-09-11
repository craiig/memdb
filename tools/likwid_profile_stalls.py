#!/usr/bin/python

# run commands to profile an app and output it to stdin
# appends 

import subprocess
import sys, re

profile_cmds = [
#	"sudo likwid-perfctr -C C1:1 -g CPI",
#	"sudo likwid-perfctr -C C1:1 -g L3CACHE",
#	"sudo likwid-perfctr -C C1:1 -g STALLS_OVERALL",
	"sudo likwid-perfctr -O -C0-1 -g STALLS1",
	"sudo likwid-perfctr -O -C0-1 -g STALLS2",
	"sudo likwid-perfctr -O -C0-1 -g STALLS3",
]
repeat_count = 1

def run_cmd(cmd):
	#runs command and echos command and command's output to a file
	#first call of run will overwrite the given file, subsequent calls to the same filename will append commands
	print "*" * 80 
	#subprocess.call("echo " + cmd, stdout=sys.stdout, shell=True)
	results = subprocess.check_output(cmd, shell=True)
	csv_start = False
	for r in results.split("\n"):
		if r == "":
			csv_start = False
		if csv_start: #ordered like this to skip the header
			yield r
		if re.match("^Event,core", r):
			csv_start = True
		print r

stall_data = []
for profile_cmd in profile_cmds:
	for i in range(repeat_count):
		cmd = profile_cmd + " " + " ".join(sys.argv[1:])
		for l in run_cmd(cmd):
			stall_data.append(l.split(","))

print "*" * 80
print stall_data

stall_data = [['DISPATCH_STALLS_SERIAL', '12418.000000', '0.000000'], ['DISPATCH_STALLS_SEGMENT_LOAD', '47211.000000', '0.000000'], ['DISPATCH_STALLS_ROB_FULL', '271315.000000', '0.000000'], ['DISPATCH_STALLS_RES_FULL', '2321654.000000', '0.000000'], ['DISPATCH_STALLS_FPU_FULL', '0.000000', '0.000000'], ['DISPATCH_STALLS_LS_FULL', '6286497.000000', '0.000000'], ['DISPATCH_STALLS_ALL_QUIT', '23370.000000', '0.000000'], ['DISPATCH_STALLS_DRAIN', '3924.000000', '0.000000'], ['DISPATCH_STALLS_BRANCH', '333656.000000', '0.000000']]
