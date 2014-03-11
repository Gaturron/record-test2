#!/usr/bin/python
import subprocess

# Run Jython with classifiers
p = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()

if p_status == 0:
	print "Command output : ", output

# Parse output

# Run RPy2 
