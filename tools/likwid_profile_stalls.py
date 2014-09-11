#!/usr/bin/python

# run commands to profile an app and output it to stdin
# appends 

import subprocess
import sys

profile_cmds = [
	"sudo likwid-perfctr -C C1:1 -g CPI",
	"sudo likwid-perfctr -C C1:1 -g L3CACHE",
	"sudo likwid-perfctr -C C1:1 -g STALLS_OVERALL",
	"sudo likwid-perfctr -C C1:1 -g STALLS1",
	"sudo likwid-perfctr -C C1:1 -g STALLS2",
	"sudo likwid-perfctr -C C1:1 -g STALLS3",
]
repeat_count = 1

def run_cmd(cmd):
	#runs command and echos command and command's output to a file
	#first call of run will overwrite the given file, subsequent calls to the same filename will append commands
	print "*" * 80 
	#subprocess.call("echo " + cmd, stdout=sys.stdout, shell=True)
	results = subprocess.call(cmd, shell=True)


for profile_cmd in profile_cmds:
	for i in range(repeat_count):
		cmd = profile_cmd + " " + " ".join(sys.argv[1:])
		run_cmd(cmd)
