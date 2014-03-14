#!/usr/bin/python
import subprocess
import re
import rpy2.robjects as robjects

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

#print output
# Parse output

lines = output.split('\n')

dataDic = {}
classifier = ''

for l in lines:

    if re.search(r'Scheme: *', l):
        classifier = re.findall(r'\w+[.]\w+ ', l)[0]
        print classifier
    if re.search(r'Correctly Classified Instances', l):
        pct = re.findall(r'\d+[.]\d+[ ]+[%]|\d+[ ]+[%]', l)[0]
        pct = pct.split(' ')[0]
        print pct
        if classifier in dataDic:
            dataDic[str(classifier)] = dataDic[str(classifier)] + [pct]
        else:
            dataDic[str(classifier)] = [pct]
    if re.search(r'Corriendo *', l):
        print l

print dataDic

# Run RPy2 
r = robjects.r

x = robjects.IntVector(range(10))
y = r.rnorm(10)

r.X11()

r.layout(r.matrix(robjects.IntVector([1,2,3,2]), nrow=2, ncol=2))
r.plot(r.runif(10), y, xlab="runif", ylab="foo/bar", col="red")