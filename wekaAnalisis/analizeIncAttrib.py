import sys

import java.io.FileReader as FileReader
import java.lang.StringBuffer as StringBuffer
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import weka.core.Instances as Instances
import weka.core.Utils as utils
import weka.filters.Filter as Filter
import weka.core.Range as Range

import weka.classifiers.trees.J48 as J48
import weka.classifiers.rules.ZeroR as ZeroR
import weka.classifiers.rules.JRip as JRip
import weka.classifiers.bayes.NaiveBayes as NaiveBayes
import weka.classifiers.functions.SMO as functionsSMO

import weka.filters.unsupervised.attribute.Remove as Remove
import weka.filters.supervised.attribute.AttributeSelection as AttributeSelection

import weka.classifiers.Evaluation as Evaluation

import weka.classifiers.meta.AttributeSelectedClassifier as AttributeSelectedClassifier

import weka.attributeSelection.CfsSubsetEval as CfsSubsetEval
import weka.attributeSelection.InfoGainAttributeEval as InfoGainAttributeEval

import weka.attributeSelection.GreedyStepwise as GreedyStepwise
import weka.attributeSelection.Ranker as Ranker

def printSummary(classifier, train, evaluation):
    print "=== Run information ===\n"
    print "Scheme: "+classifier.getClass().getName()+" "+utils.joinOptions(classifier.getOptions())
    print "Relation: "+str(train.relationName())
    print "Instances: "+str(train.numInstances())
    print "Attributes: "+str(train.numAttributes())+"\n" 

    print "=== Classifier model ===\n"
    print classifier

    print "=== Summary ==="
    print evaluation.toSummaryString()
    print evaluation.toClassDetailsString()
    print evaluation.toMatrixString()

def runZeroR(train, test):
    zeroR = ZeroR()
    zeroR.setDebug(True)

    zeroR.buildClassifier(train)
    evaluation = Evaluation(train)

    evaluation.evaluateModel(zeroR, test)
    printSummary(zeroR, train, evaluation)

def runJRip(train, test):
    jrip = JRip()
    jrip.setDebug(True)
    jrip.setOptions(['-F 3', '-N 2.0', '-O 2', '-S 1'])

    jrip.buildClassifier(train)
    evaluation = Evaluation(train)

    evaluation.evaluateModel(jrip, test)
    printSummary(jrip, train, evaluation)

def filterByAttributes(attributesToDelete, train, test):
    listAttributeTrain = []
    for att in attributesToDelete:
        listAttributeTrain.append(train.attribute(att).index())

    listAttributeTest = []
    for att in attributesToDelete:
        listAttributeTest.append(test.attribute(att).index())

    removeTrain = Remove()
    removeTrain.setAttributeIndicesArray(listAttributeTrain)
    removeTrain.setInputFormat(train)
    train1 = Filter.useFilter(train, removeTrain)

    removeTest = Remove()
    removeTest.setAttributeIndicesArray(listAttributeTest)
    removeTest.setInputFormat(test)
    test1 = Filter.useFilter(test, removeTest)	

    return (train1, test1)

if len(sys.argv) != 2:
    print "Pasar como parametro el path de los tests"
    print "Por ejemplo: /home/fernando/Tesis/record-test2/attributeExtractor/tests/"
    sys.exit(0)
    
#path = "/home/fernando/Tesis/record-test2/attributeExtractor/tests/"
path = sys.argv[1]
i = 1

file = FileReader(path+"train"+str(i)+".arff")
train = Instances(file)
train.setClassIndex(train.attribute('place').index())

file = FileReader(path+"test"+str(i)+".arff")
test = Instances(file)
test.setClassIndex(test.attribute('place').index())

print "Corriendo paired wilcoxon tests: train"+str(i)+" test"+str(i)
print "====================================================================="
print "Baseline"

(train1, test1) = (train, test)
runZeroR(train1, test1)

print "JRip con atributos de SIL + FON + ACU"
runJRip(train1, test1)

#calculos previos
acuAtt = [ "MFCC_"+size+type+"_"+str(i) 
            for i in range(12+1) 
            for size in ["Min", "Average", "Max"] 
            for type in ["KT", "LL", "RR", "SC"]     ]

silAtt = [ "SIL_"+type+"_"+norm
            for type in ["prevSyllableAccent", "syllableAccent" ] 
            for norm in ["norm", "normhd"]      ]

fonAtt = ["PHO_"+type+"_"+norm
            for type in ["Sfinal", "consonant", "kt", "ll", "rr", "sc", "vowel"]
            for norm in ["norm", "normhd"]      ]

print "JRip con atributos de SIL + FON"
attributesToDelete = acuAtt
(train1, test1) = filterByAttributes(attributesToDelete, train, test)
train1.setClassIndex(train1.attribute('place').index())
test1.setClassIndex(test1.attribute('place').index())
runJRip(train1, test1)

print "JRip con atributos de FON + ACU"
attributesToDelete = silAtt
(train1, test1) = filterByAttributes(attributesToDelete, train, test)
train1.setClassIndex(train1.attribute('place').index())
test1.setClassIndex(test1.attribute('place').index())
runJRip(train1, test1)

print "JRip con atributos de SIL"
attributesToDelete = acuAtt ++ fonAtt
(train1, test1) = filterByAttributes(attributesToDelete, train, test)
train1.setClassIndex(train1.attribute('place').index())
test1.setClassIndex(test1.attribute('place').index())
runJRip(train1, test1)

print "JRip con atributos de FON"
attributesToDelete = acuAtt ++ silAtt
(train1, test1) = filterByAttributes(attributesToDelete, train, test)
train1.setClassIndex(train1.attribute('place').index())
test1.setClassIndex(test1.attribute('place').index())
runJRip(train1, test1)

print "JRip con atributos de ACU"
attributesToDelete = silAtt ++ fonAtt 
(train1, test1) = filterByAttributes(attributesToDelete, train, test)
train1.setClassIndex(train1.attribute('place').index())
test1.setClassIndex(test1.attribute('place').index())
runJRip(train1, test1)