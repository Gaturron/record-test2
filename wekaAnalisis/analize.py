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
import weka.filters.unsupervised.attribute.Remove as Remove
import weka.classifiers.Evaluation as Evaluation
import weka.classifiers.meta.AttributeSelectedClassifier as AttributeSelectedClassifier
import weka.attributeSelection.CfsSubsetEval as CfsSubsetEval
import weka.attributeSelection.GreedyStepwise as GreedyStepwise

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
folds = 10

jrip.buildClassifier(data1)

rand = Random(1); 
evaluation.crossValidateModel(jrip, data1, folds, rand );

print "Baseline:\n==========\n"
print jrip
print evaluation.toSummaryString()
print evaluation.toMatrixString()

print "======================================================================"
# ============================================================================
# Calculando las alternativas
# ===========================
# Seleccionando atributos con Greedy Stepwise

listAttribute = []
listAttribute.append(data.attribute('phrases').index())

remove = Remove()
remove.setAttributeIndicesArray(listAttribute)
remove.setInvertSelection(False) 
#False: para que borre los atributos definidos
remove.setInputFormat(data)
data2 = Filter.useFilter(data, remove)
data2.setClassIndex(data2.attribute('place').index())

evalu = CfsSubsetEval()
search = GreedyStepwise()
search.setSearchBackwards(True)
j48 = J48()

classifier = AttributeSelectedClassifier()
classifier.setClassifier(j48)
classifier.setEvaluator(evalu)
classifier.setSearch(search)

evaluation = Evaluation(data2)
# 10-fold cross-validation
evaluation.crossValidateModel(classifier, data2, 10, Random(1))
print "GreedyStepwise(CfsSubsetEval):\n===============================\n"
print j48
print evaluation.toSummaryString()
print evaluation.toMatrixString()