#!/usr/bin/python
from numpy  import *
from decimal import Decimal

import subprocess
import re
import sys
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri

from rpy2.robjects.packages import importr

if len(sys.argv) != 2:
    print "Pasar como parametro el path de los tests"
    print "Por ejemplo: /home/fernando/Tesis/record-test2/attributeExtractor/tests/"
    sys.exit(0)

rpy2.robjects.numpy2ri.activate()

# Run Jython with classifiers
p = subprocess.Popen(
    """
    export CLASSPATH=$CLASSPATH:/home/fernando/Tesis/weka-3-6-10/weka.jar; 
    jython analize1.py """+ sys.argv[1] +"""
    """, stdout=subprocess.PIPE, shell=True)

(output, err) = p.communicate()
p_status = p.wait()

if p_status != 0:
    print 'ERROR: '+str(err)

#print "Output:"
#print output

# Parse output

lines = output.split('\n')

dataDic = {}
classifier = ''

for l in lines:

    if re.search(r'Scheme: *', l):
        classifier = re.findall(r'\w+[.]\w+ ', l)[0].strip()
        print classifier
    if re.search(r'Correctly Classified Instances', l):
        pct = re.findall(r'\d+[.]\d+[ ]+[%]|\d+[ ]+[%]', l)[0]
        pct = pct.split(' ')[0]
        print pct
        if classifier in dataDic:
            dataDic[str(classifier)] = dataDic[str(classifier)] + [double(pct)]
        else:
            dataDic[str(classifier)] = [double(pct)]
    if re.search(r'Corriendo *', l):
        print l

print dataDic

# Run RPy2 
print '\n\nVector para R:'
r = robjects.r

ZeroR = robjects.FloatVector(array(dataDic['rules.ZeroR']))
print 'ZeroR '+str(ZeroR)

JRip = robjects.FloatVector(array(dataDic['rules.JRip']))
print 'JRip: '+str(JRip)

J48 = robjects.FloatVector(array(dataDic['trees.J48']))
print 'J48 '+str(J48)

NaiveBayes = robjects.FloatVector(array(dataDic['bayes.NaiveBayes']))
print 'NaiveBayes '+str(NaiveBayes)

SMO = robjects.FloatVector(array(dataDic['functions.SMO']))
print 'SMO '+str(SMO)

print '=================================================================='

shapiro_test = r('shapiro.test')

ZeroR_pvalue = shapiro_test(ZeroR)[1]
JRip_pvalue = shapiro_test(JRip)[1]
J48_pvalue = shapiro_test(J48)[1]
NaiveBayes_pvalue = shapiro_test(NaiveBayes)[1]
SMO_pvalue = shapiro_test(SMO)[1]

t_test = r('t.test')
if (ZeroR_pvalue > 0.05 and JRip_pvalue > 0.05):
    print t_test(ZeroR, JRip, paired=True, alternative="less")
if (ZeroR_pvalue > 0.05 and J48_pvalue > 0.05):
    print t_test(ZeroR, J48, paired=True, alternative="less")
if (ZeroR_pvalue > 0.05 and NaiveBayes_pvalue > 0.05):
    print t_test(ZeroR, NaiveBayes, paired=True, alternative="less")
if (ZeroR_pvalue > 0.05 and SMO_pvalue > 0.05):
    print t_test(ZeroR, SMO, paired=True, alternative="less")

wilcox_test = r('wilcox.test')

print  wilcox_test(ZeroR, JRip, paired=True, alternative="less")
print  wilcox_test(ZeroR, J48, paired=True, alternative="less")
print  wilcox_test(ZeroR, NaiveBayes, paired=True, alternative="less")
print  wilcox_test(ZeroR, SMO, paired=True, alternative="less")