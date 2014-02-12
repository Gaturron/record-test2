import sys

import java.io.FileReader as FileReader
import java.lang.StringBuffer as StringBuffer
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import weka.core.Instances as Instances
import weka.filters.Filter as Filter
import weka.core.Range as Range

import weka.classifiers.trees.J48 as J48
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

# load data file
file = FileReader("/home/fernando/Tesis/record-test2/attributeExtractor/test1.numeric.arff")
data = Instances(file)
#data.setClassIndex(data.numAttributes() - 1)

# Calculando el Baseline
# ======================

listAttribute = []
listAttribute.append(data.attribute('durationAvgOfPrevSyllable').index())
listAttribute.append(data.attribute('duration').index())
listAttribute.append(data.attribute('place').index())

remove = Remove()
remove.setAttributeIndicesArray(listAttribute)
remove.setInvertSelection(True) 
#True: para que mantenga los atributos definidos
remove.setInputFormat(data)
data1 = Filter.useFilter(data, remove)
data1.setClassIndex(data1.attribute('place').index())

jrip = JRip()
jrip.setDebug(True)
jrip.setOptions(['-F 3', '-N 2.0', '-O 2', '-S 1'])

evaluation = Evaluation(data1)

jrip.buildClassifier(data1)

evaluation.crossValidateModel(jrip, data1, 10, Random(1));

print "Baseline:\n==========\n"
print jrip
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "======================================================================"
# ============================================================================
print "Calculando las alternativas"
print "==========================="
print "Seleccionando atributos con Greedy Stepwise"
print "==========================================="

listAttribute = []
listAttribute.append(data.attribute('phrases').index())

remove = Remove()
remove.setAttributeIndicesArray(listAttribute)
remove.setInvertSelection(False) 
#False: para que borre los atributos definidos
remove.setInputFormat(data)
dataTmp = Filter.useFilter(data, remove)
dataTmp.setClassIndex(dataTmp.attribute('place').index())

filter = AttributeSelection()
evalu = CfsSubsetEval()
search = GreedyStepwise()
search.setSearchBackwards(True)
filter.setEvaluator(evalu)
filter.setSearch(search)
filter.setInputFormat(dataTmp)
filteredData = Filter.useFilter(dataTmp, filter)

print "Atributos seleccionados:"
for i, att in enumerate(filteredData.enumerateAttributes()):
    print str(i) +") "+ str(att)

print "--------------------------------------------"
j48 = J48()
classifier = AttributeSelectedClassifier()
classifier.setClassifier(j48)
classifier.setEvaluator(evalu)
classifier.setSearch(search)

evaluation = Evaluation(filteredData)
# 10-fold cross-validation
evaluation.crossValidateModel(classifier, filteredData, 10, Random(1))

print "GreedyStepwise(CfsSubsetEval) con J48:\n===============================\n"
print j48
print evaluation.toSummaryString()
print evaluation.toMatrixString()

# --------------------------------------------
jrip = JRip()
jrip.setDebug(True)
jrip.setOptions(['-F 3', '-N 2.0', '-O 2', '-S 1'])

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(jrip, filteredData, 10, Random(1))
print "GreedyStepwise(CfsSubsetEval) con JRip:\n===============================\n"
print jrip
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
print "Seleccionando atributos con Ranker"
print "==========================================="
numAtt = 10
print "Cant. de attributos: "+str(numAtt)

listAttribute = []
listAttribute.append(data.attribute('phrases').index())

remove = Remove()
remove.setAttributeIndicesArray(listAttribute)
remove.setInvertSelection(False) 
#False: para que borre los atributos definidos
remove.setInputFormat(data)
dataTmp = Filter.useFilter(data, remove)
dataTmp.setClassIndex(dataTmp.attribute('place').index())

filter = AttributeSelection()
evalu = InfoGainAttributeEval()
search = Ranker()
search.setNumToSelect(numAtt) 
filter.setEvaluator(evalu)
filter.setSearch(search)

filter.setInputFormat(dataTmp)
filteredData = Filter.useFilter(dataTmp, filter)

print "Atributos seleccionados:"
for i, att in enumerate(filteredData.enumerateAttributes()):
    print str(i) +") "+ str(att)

print "--------------------------------------------"
j48 = J48()
classifier = AttributeSelectedClassifier()
classifier.setClassifier(j48)
classifier.setEvaluator(evalu)
classifier.setSearch(search)

evaluation = Evaluation(filteredData)
# 10-fold cross-validation
evaluation.crossValidateModel(classifier, filteredData, 10, Random(1))

print "Ranker(InfoGain) con J48:\n===============================\n"
print j48
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
jrip = JRip()
jrip.setDebug(True)
jrip.setOptions(['-F 3', '-N 2.0', '-O 2', '-S 1'])

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(jrip, filteredData, 10, Random(1))

print "Ranker(InfoGain) con JRip:\n===============================\n"
print jrip
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
naiveBayes = NaiveBayes()
naiveBayes.setDebug(True)

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(naiveBayes, filteredData, 10, Random(1))

print "Ranker(InfoGain) con NaiveBayes:\n===============================\n"
print naiveBayes
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
functSMO = functionsSMO()
functSMO.setDebug(True)

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(functSMO, filteredData, 10, Random(1))

print "Ranker(InfoGain) con functionsSMO:\n===============================\n"
print functSMO
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "==========================================="
numAtt = 20
print "Cant. de attributos: "+str(numAtt)

listAttribute = []
listAttribute.append(data.attribute('phrases').index())

remove = Remove()
remove.setAttributeIndicesArray(listAttribute)
remove.setInvertSelection(False) 
#False: para que borre los atributos definidos
remove.setInputFormat(data)
dataTmp = Filter.useFilter(data, remove)
dataTmp.setClassIndex(dataTmp.attribute('place').index())

filter = AttributeSelection()
evalu = InfoGainAttributeEval()
search = Ranker()
search.setNumToSelect(numAtt) 
filter.setEvaluator(evalu)
filter.setSearch(search)

filter.setInputFormat(dataTmp)
filteredData = Filter.useFilter(dataTmp, filter)

print "Atributos seleccionados:"
for i, att in enumerate(filteredData.enumerateAttributes()):
    print str(i) +") "+ str(att)

print "--------------------------------------------"
j48 = J48()
classifier = AttributeSelectedClassifier()
classifier.setClassifier(j48)
classifier.setEvaluator(evalu)
classifier.setSearch(search)

evaluation = Evaluation(filteredData)
# 10-fold cross-validation
evaluation.crossValidateModel(classifier, filteredData, 10, Random(1))

print "Ranker(InfoGain) con J48:\n===============================\n"
print j48
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
jrip = JRip()
jrip.setDebug(True)
jrip.setOptions(['-F 3', '-N 2.0', '-O 2', '-S 1'])

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(jrip, filteredData, 10, Random(1))

print "Ranker(InfoGain) con JRip:\n===============================\n"
print jrip
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
naiveBayes = NaiveBayes()
naiveBayes.setDebug(True)

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(naiveBayes, filteredData, 10, Random(1))

print "Ranker(InfoGain) con NaiveBayes:\n===============================\n"
print naiveBayes
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
functSMO = functionsSMO()
functSMO.setDebug(True)

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(functSMO, filteredData, 10, Random(1))

print "Ranker(InfoGain) con functionsSMO:\n===============================\n"
print functSMO
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "==========================================="
numAtt = 30
print "Cant. de attributos: "+str(numAtt)

listAttribute = []
listAttribute.append(data.attribute('phrases').index())

remove = Remove()
remove.setAttributeIndicesArray(listAttribute)
remove.setInvertSelection(False) 
#False: para que borre los atributos definidos
remove.setInputFormat(data)
dataTmp = Filter.useFilter(data, remove)
dataTmp.setClassIndex(dataTmp.attribute('place').index())

filter = AttributeSelection()
evalu = InfoGainAttributeEval()
search = Ranker()
search.setNumToSelect(numAtt) 
filter.setEvaluator(evalu)
filter.setSearch(search)

filter.setInputFormat(dataTmp)
filteredData = Filter.useFilter(dataTmp, filter)

print "Atributos seleccionados:"
for i, att in enumerate(filteredData.enumerateAttributes()):
    print str(i) +") "+ str(att)

print "--------------------------------------------"
j48 = J48()
classifier = AttributeSelectedClassifier()
classifier.setClassifier(j48)
classifier.setEvaluator(evalu)
classifier.setSearch(search)

evaluation = Evaluation(filteredData)
# 10-fold cross-validation
evaluation.crossValidateModel(classifier, filteredData, 10, Random(1))

print "Ranker(InfoGain) con J48:\n===============================\n"
print j48
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
jrip = JRip()
jrip.setDebug(True)
jrip.setOptions(['-F 3', '-N 2.0', '-O 2', '-S 1'])

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(jrip, filteredData, 10, Random(1))

print "Ranker(InfoGain) con JRip:\n===============================\n"
print jrip
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
naiveBayes = NaiveBayes()
naiveBayes.setDebug(True)

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(naiveBayes, filteredData, 10, Random(1))

print "Ranker(InfoGain) con NaiveBayes:\n===============================\n"
print naiveBayes
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
functSMO = functionsSMO()
functSMO.setDebug(True)

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(functSMO, filteredData, 10, Random(1))

print "Ranker(InfoGain) con functionsSMO:\n===============================\n"
print functSMO
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "==========================================="
numAtt = 40
print "Cant. de attributos: "+str(numAtt)

listAttribute = []
listAttribute.append(data.attribute('phrases').index())

remove = Remove()
remove.setAttributeIndicesArray(listAttribute)
remove.setInvertSelection(False) 
#False: para que borre los atributos definidos
remove.setInputFormat(data)
dataTmp = Filter.useFilter(data, remove)
dataTmp.setClassIndex(dataTmp.attribute('place').index())

filter = AttributeSelection()
evalu = InfoGainAttributeEval()
search = Ranker()
search.setNumToSelect(numAtt) 
filter.setEvaluator(evalu)
filter.setSearch(search)

filter.setInputFormat(dataTmp)
filteredData = Filter.useFilter(dataTmp, filter)

print "Atributos seleccionados:"
for i, att in enumerate(filteredData.enumerateAttributes()):
    print str(i) +") "+ str(att)

print "--------------------------------------------"
j48 = J48()
classifier = AttributeSelectedClassifier()
classifier.setClassifier(j48)
classifier.setEvaluator(evalu)
classifier.setSearch(search)

evaluation = Evaluation(filteredData)
# 10-fold cross-validation
evaluation.crossValidateModel(classifier, filteredData, 10, Random(1))

print "Ranker(InfoGain) con J48:\n===============================\n"
print j48
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
jrip = JRip()
jrip.setDebug(True)
jrip.setOptions(['-F 3', '-N 2.0', '-O 2', '-S 1'])

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(jrip, filteredData, 10, Random(1))

print "Ranker(InfoGain) con JRip:\n===============================\n"
print jrip
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
naiveBayes = NaiveBayes()
naiveBayes.setDebug(True)

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(naiveBayes, filteredData, 10, Random(1))

print "Ranker(InfoGain) con NaiveBayes:\n===============================\n"
print naiveBayes
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
functSMO = functionsSMO()
functSMO.setDebug(True)

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(functSMO, filteredData, 10, Random(1))

print "Ranker(InfoGain) con functionsSMO:\n===============================\n"
print functSMO
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "==========================================="
numAtt = 80
print "Cant. de attributos: "+str(numAtt)

listAttribute = []
listAttribute.append(data.attribute('phrases').index())

remove = Remove()
remove.setAttributeIndicesArray(listAttribute)
remove.setInvertSelection(False) 
#False: para que borre los atributos definidos
remove.setInputFormat(data)
dataTmp = Filter.useFilter(data, remove)
dataTmp.setClassIndex(dataTmp.attribute('place').index())

filter = AttributeSelection()
evalu = InfoGainAttributeEval()
search = Ranker()
search.setNumToSelect(numAtt) 
filter.setEvaluator(evalu)
filter.setSearch(search)

filter.setInputFormat(dataTmp)
filteredData = Filter.useFilter(dataTmp, filter)

print "Atributos seleccionados:"
for i, att in enumerate(filteredData.enumerateAttributes()):
    print str(i) +") "+ str(att)

print "--------------------------------------------"
j48 = J48()
classifier = AttributeSelectedClassifier()
classifier.setClassifier(j48)
classifier.setEvaluator(evalu)
classifier.setSearch(search)

evaluation = Evaluation(filteredData)
# 10-fold cross-validation
evaluation.crossValidateModel(classifier, filteredData, 10, Random(1))

print "Ranker(InfoGain) con J48:\n===============================\n"
print j48
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
jrip = JRip()
jrip.setDebug(True)
jrip.setOptions(['-F 3', '-N 2.0', '-O 2', '-S 1'])

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(jrip, filteredData, 10, Random(1))

print "Ranker(InfoGain) con JRip:\n===============================\n"
print jrip
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
naiveBayes = NaiveBayes()
naiveBayes.setDebug(True)

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(naiveBayes, filteredData, 10, Random(1))

print "Ranker(InfoGain) con NaiveBayes:\n===============================\n"
print naiveBayes
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "--------------------------------------------"
functSMO = functionsSMO()
functSMO.setDebug(True)

evaluation = Evaluation(filteredData)

jrip.buildClassifier(filteredData)

evaluation.crossValidateModel(functSMO, filteredData, 10, Random(1))

print "Ranker(InfoGain) con functionsSMO:\n===============================\n"
print functSMO
print evaluation.toSummaryString()
print evaluation.toMatrixString()

