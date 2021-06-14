#!/usr/bin/env python3

import os.path, subprocess, sys, argparse, re, time

A_ScriptDir = os.path.dirname(os.path.realpath(__file__))
A_WorkingDir = os.getcwd()

temperature_regex = re.compile("\+\d+(\.\d+)?°C")

def run_with_output(cmd, shell = False):
	output = ""
	p = subprocess.Popen(cmd, shell = shell, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True)
	while p.poll() is None:
		line = p.stdout.readline()
		#print(line, end = "")
		output += line
	p.stdout.close()
	p.wait()
	
	if(p.returncode != 0):
		print("error")
		sys.exit(p.returncode)
	
	return output


def get_temperature():
	match = temperature_regex.search(run_with_output("sensors | grep temp1:", shell = True))
	if(match):
		return match.group(0)
	return ""


def collect_samples(timeout = 100, interval = 10):
	open("temps", "w").close()
	start = time.time_ns()
	timeout *= 60 * 1e9
	
	while(timeout == 0 or time.time_ns() - start < timeout):
		try:
			temp = get_temperature()
			print(temp)
			f = open("temps", "a")
			f.write(temp + "\n")
			f.close()
			time.sleep(interval)
		except IOError:
			time.sleep(0.1)

def main():
	parser = argparse.ArgumentParser(description = "Script to check the CPU temerature.")
	
	parser.add_argument("-i", "--interval", metavar = "NUMBER", default = 10, type = int, help = "set interval between each sample in secounds (10s)")
	parser.add_argument("-t", "--timeout", metavar = "NUMBER", default = -1, type = int, help = "set duration where the samples will be collected in minuts, set to 0 for no timeout (-1)")
	
	args = parser.parse_args()
	#try:
	if(args.timeout == -1):
		print(get_temperature())
	else:
		collect_samples(timeout = args.timeout, interval = args.interval)
	#except:
	#	pass
	
if __name__ == "__main__":
	main()
