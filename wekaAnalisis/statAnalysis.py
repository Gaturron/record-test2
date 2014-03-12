#!/usr/bin/python
import subprocess
import re

# Run Jython with classifiers
p = subprocess.Popen(
	"""
	export CLASSPATH=$CLASSPATH:/home/fernando/Tesis/weka-3-6-10/weka.jar; 
	jython analize1.py
	""", stdout=subprocess.PIPE, shell=True)

(output, err) = p.communicate()
p_status = p.wait()

if p_status != 0:
	print 'ERROR: '+str(err)

print output

# Parse output

lines = output.split('\n')
for l in lines:
	if re.search(r'Correctly Classified Instances|(Scheme: *)|(Corriendo *)', l):
		print l

# Run RPy2 
