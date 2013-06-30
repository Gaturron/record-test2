import subprocess

s1 = "localhost:8000"
s2 = "elgatoloco.no-ip.org"
dir = "~/Tesis/record-test2/audios/static/js/record_functions.js ~/Tesis/record-test2/audios/templates/record_tests.html ~/Tesis/record-test2/audios/templates/record_tests1.html"

proc1 = subprocess.Popen("grep -o "+str(s1)+" "+str(dir)+" -r  | wc -l", stdout=subprocess.PIPE, shell=True)
(out1, err1) = proc1.communicate()
if err1: print "Check script: "+str(err1)
out1 = int(out1)

proc2 = subprocess.Popen("grep -o "+str(s2)+" "+str(dir)+" -r  | wc -l", stdout=subprocess.PIPE, shell=True)
(out2, err2) = proc2.communicate()
if err2: print "Check script: "+str(err2)
out2 = int(out2)

#Uno debe dar 0 (o deberia)
if ((out1 != 0 and out2 == 0) or (out1 == 0 and out2 != 0)):
	
	if (out2 != 0):
		#swap
		swap = s1
		s1 = s2
		s2 = swap

	print "Replacing: "+s1+" -> "+s2
	proc = subprocess.Popen("find "+str(dir)+" -type f -exec sed -i 's/"+s1+"/"+s2+"/g' {} \;", stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()

	if err: 
		print "Error replacing: "+str(err)	
	else: 
		print "OK!"
else:
	print "Check script"





