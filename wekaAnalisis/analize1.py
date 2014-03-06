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

def runJ48(train, test):
    j48 = J48()
    j48.setDebug(True)

    j48.buildClassifier(train)
    evaluation = Evaluation(train)

    evaluation.evaluateModel(j48, test)
    printSummary(j48, train, evaluation)

def runFunctSMO(train, test):
    functSMO = functionsSMO()
    functSMO.setDebug(True)

    functSMO.buildClassifier(train)
    evaluation = Evaluation(train)

    evaluation.evaluateModel(functSMO, test)
    printSummary(functSMO, train, evaluation)

def runNaiveBayes(train, test):
    naiveBayes = NaiveBayes()
    naiveBayes.setDebug(True)

    naiveBayes.buildClassifier(train)
    evaluation = Evaluation(train)

    evaluation.evaluateModel(naiveBayes, test)
    printSummary(naiveBayes, train, evaluation)


for i in range(10):

    #path = "/home/fernando/Tesis/record-test2/attributeExtractor/tests/"
    path = "/home/fernando/Tesis/record-test2/attributeExtractor/tests2/"

    file = FileReader(path+"train"+str(i)+".arff")
    train = Instances(file)
    train.setClassIndex(train.attribute('place').index())

    file = FileReader(path+"test"+str(i)+".arff")
    test = Instances(file)
    test.setClassIndex(test.attribute('place').index())

    print "Corriendo paired wilcoxon tests: train"+str(i)+" test"+str(i)
    print "====================================================================="
    runZeroR(train, test)
    runJRip(train, test)
    runJ48(train, test)
    runFunctSMO(train, test)
    runNaiveBayes(train, test)